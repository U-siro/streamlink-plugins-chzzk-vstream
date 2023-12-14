# Copyright Renai Entertainment, Licensed under AGPL 3.0
# Streamlink VStream

import re
from streamlink.plugin import Plugin, pluginargument, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream, HLSStreamReader, HLSStreamWriter


import logging
import json

log = logging.getLogger(__name__)

@pluginmatcher(re.compile(r"https?://(?:www\.)?vstream\.com/c/(.*)$"))


class vstream(Plugin):
    def _get_streams(self):
        streams = {}
 
        # Retrieve the stream URL from the website
        # In this example, we assume the stream URL is "https://example.com/stream.m3u8"
        #log.debug(self.url)
        res = self.session.http.get(self.url).text
        log.debug(res.split('remixContext')[1][3:-3])
        res_data = json.loads(res.split('remixContext')[1][3:-3])
        #log.debug(res_data)
        if res_data["state"]["loaderData"]["routes/_app.c.$username._index"]["channelProfile"]["liveStreaming"]["ongoingLiveStream"] == None:
            return

        
        stream_url = res_data["state"]["loaderData"]["routes/_app.c.$username._index"]["channelProfile"]["liveStreaming"]["ongoingLiveStream"]["manifestURL"] 
        self.author = res_data["state"]["loaderData"]["routes/_app.c.$username._index"]["channelProfile"]["userProfile"]["displayName"] 
        self.title = res_data["state"]["loaderData"]["routes/_app.c.$username._index"]["channelProfile"]["liveStreaming"]["ongoingLiveStream"]["title"]
        self.id = res_data["state"]["loaderData"]["routes/_app.c.$username._index"]["channelProfile"]["liveStreaming"]["ongoingLiveStream"]["id"]
        # Create an HLSStream object with the stream URL
        hls_stream = HLSStream.parse_variant_playlist(self.session, stream_url)
 
        # Add the HLS stream to the streams dictionary
        streams = hls_stream
 
        return streams
    
__plugin__= vstream