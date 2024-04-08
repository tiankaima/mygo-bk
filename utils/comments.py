import urllib3
import requests
import json
import aiohttp
import asyncio
import bilibili_api
import os
from bilibili_api import Credential, comment, sync
from bilibili_api.video import Video
from pprint import pprint

credential = bilibili_api.Credential(
    sessdata="",
    bili_jct="",
    buvid3="",
)

BV_ids = [
    "BV1Zu4y1B7DU",
    "BV1xV41137an",
    "BV1nV41137kJ",
    "BV14V4y1v7pb",
    "BV1ah4y1k7jm",
    "BV1eh4y1k78d",
    "BV1dj411z7FW",
    "BV1k94y1r7o1",
    "BV1M8411d7Dj",
    "BV1Wm4y1H7Vt",
    "BV11F411C79G",
    "BV1Vm4y1M7mX",
    "BV1iz4y1j7xY",
]

vids = [bilibili_api.video.Video(bvid=bvid, credential=credential) for bvid in BV_ids]


async def fetch_comment_replies(comment: comment.Comment) -> list[dict]:
    replies = []
    page = 1
    count = 0
    while True:
        r = await comment.get_sub_comments(
            page_index=page,
        )
        await asyncio.sleep(0.1)
        if r["replies"] is None:
            break
        replies.extend(r["replies"])
        count += r["page"]["size"]
        page += 1
        if count >= r["page"]["count"]:
            break

    return replies


async def fetch_video_comment(video: Video) -> None:
    id = BV_ids.index(video.get_bvid()) + 1
    path = f"./export/{id}.json"

    comments = []
    page = 1
    count = 0
    while True:
        c = await comment.get_comments(
            video.get_aid(),
            comment.CommentResourceType.VIDEO,
            page_index=page,
            order=comment.OrderType.LIKE,
            credential=credential,
        )
        await asyncio.sleep(0.1)

        for _c in c["replies"]:
            if _c["rcount"] > 3:
                _c["replies"] = await fetch_comment_replies(
                    comment.Comment(
                        oid=_c["oid"],
                        type_=comment.CommentResourceType.VIDEO,
                        rpid=_c["rpid"],
                    )
                )
            count += _c["rcount"]

        comments.extend(c["replies"])
        count += c["page"]["size"]
        page += 1
        print(page, count, c["page"]["count"])

        if count >= c["page"]["count"]:
            break

        with open(path, "w") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)


async def main() -> None:
    for vid in vids:
        try:
            info = await vid.get_info()
            await fetch_video_comment(vid)
        except Exception as e:
            print(e)


loop = asyncio.get_event_loop()
loop.create_task(main())
