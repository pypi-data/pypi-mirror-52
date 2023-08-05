import asyncio
import logging

from zeta import crypto
from zeta.db import headers

from typing import Any, Callable, Optional
from zeta.zeta_types import TransactionEntry

LOGGER: logging.Logger


def set_logger(name: str):  # pragma: nocover
    global LOGGER
    try:
        LOGGER
        raise RuntimeError('App logger has already been set')
    except NameError:
        LOGGER = logging.getLogger(name)


def get_logger() -> logging.Logger:  # pragma: nocover
    return LOGGER


def reverse_hex(h: str):
    '''Reverses a hex-serialized bytestring'''
    return bytes.fromhex(h)[::-1].hex()


async def queue_logger(
        q: asyncio.Queue,
        transform: Optional[Callable[[Any], Any]] = None) -> None:  # pragma: nocover  # noqa: E501
    '''
    Logs a queue as entries come in
    Useful for debugging

    Args:
        q (asyncio.Queue): the queue to log
    '''
    LOGGER.info('registering queue logger')

    def do_nothing(k: Any) -> Any:
        return k
    t = transform if transform is not None else do_nothing
    while True:
        LOGGER.info(t(await q.get()))


async def queue_forwarder(
        inq: asyncio.Queue,
        outq: asyncio.Queue,
        transform: Optional[Callable[[Any], Any]] = None) -> None:  # pragma: nocover  # noqa: E501
    '''
    Forwards everything from a queue to another queue
    Useful for combining queues

    Args:
        inq  (asyncio.Queue): input queue
        outq (asyncio.Queue): output queue
        transform (function): A function to transform the q items with

    '''
    def do_nothing(k: Any) -> Any:
        return k
    t = transform if transform is not None else do_nothing
    while True:
        msg = await inq.get()
        await outq.put(t(msg))


async def _report_best_block() -> None:
    '''
    Logs stats about the heaviest (best) block every 10 seconds
    '''
    best = None
    while True:
        heaviest = headers.find_heaviest()

        # it'd be very strange if this failed
        # but I put in the check, which implies that it happened in testing
        if len(heaviest) != 0:
            if best and heaviest[0]['height'] > best['height']:
                LOGGER.info('chain tip advanced {} block(s)'.format(
                    heaviest[0]['height'] - best['height']
                ))
            best = heaviest[0]
            LOGGER.info('Best Block: {} at {} with {} work'.format(
                best['hash'],
                best['height'],
                best['accumulated_work']
            ))
        await asyncio.sleep(15)


async def _report_new_headers(header_q) -> None:
    # log header hashes as they come in
    def make_block_hash(h) -> str:
        # log the header hash in a human-readable format
        return('new header: {}'.format(
            crypto.hash256(bytes.fromhex(h['hex']))[::-1].hex()))
    asyncio.ensure_future(queue_logger(header_q, make_block_hash))


async def _report_new_prevouts(prevout_q) -> None:
    def humanize_prevout(prevout) -> str:
        if prevout['spent_at'] == -2:
            return('new prevout: {} sat at {} in {}...{}'.format(
                prevout['value'],
                prevout['address'][:12],
                prevout['outpoint']['tx_id'][:8],
                prevout['outpoint']['index']))
        else:
            return('spent prevout: {} sat at {} in {}...{} block {}'.format(
                prevout['value'],
                prevout['address'][:12],
                prevout['outpoint']['tx_id'][:8],
                prevout['outpoint']['index'],
                prevout['spent_at']))
    asyncio.ensure_future(queue_logger(prevout_q, humanize_prevout))


async def _report_new_txns(tx_q: 'asyncio.Queue[TransactionEntry]') -> None:
    def humanize_tx(tx: TransactionEntry) -> str:
        return ('tx store updated: {} at height {} is {}'.format(
            tx['tx_id'],
            tx['confirmed_height'],
            'verified' if tx['merkle_verified'] else 'not verified'))
    asyncio.ensure_future(queue_logger(tx_q, humanize_tx))
