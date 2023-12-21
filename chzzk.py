# Copyright Renai Entertainment, Licensed under AGPL 3.0
# Streamlink Chzzk

import re
from streamlink.plugin import Plugin, pluginargument, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream, HLSStreamReader, HLSStreamWriter


import logging
import json

log = logging.getLogger(__name__)

@pluginmatcher(re.compile(r"https?://(?:www\.)?chzzk\.naver\.com/(?:live/)(?P<username>\w+)$"))

class chzzk(Plugin):
    def _get_streams(self):

        m = self.match.groupdict()
        username = m["username"]

        streams = {}
 
        # Retrieve the stream URL from the website
        # In this example, we assume the stream URL is "https://example.com/stream.m3u8"
        #log.debug(self.url)
        res = self.session.http.get("https://api.chzzk.naver.com/service/v1/channels/" + username + "/live-detail").text
        #log.debug(res.split('remixContext')[1][3:-3])
        res_data = json.loads(res)
        #log.debug(res_data)
        if res_data["content"] == None:
            return
        res_data_playback = json.loads(res_data["content"]["livePlaybackJson"])
        self.author = res_data["content"]["channel"]["channelName"]
        self.id = res_data["content"]["liveId"]
        self.title = res_data["content"]["liveTitle"]
        self.category = res_data["content"]["liveCategoryValue"]
        # Create an HLSStream object with the stream URL
        hls_stream = HLSStream.parse_variant_playlist(self.session, res_data_playback["media"][0]["path"])
    
        # Add the HLS stream to the streams dictionary
        streams = hls_stream
 
        return streams
    
__plugin__= chzzk