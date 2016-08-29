import logging
import os
import sys
import threading

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_media.protocolentities import *

name="test"
logger = logging.getLogger(name)

class SendMedia(YowInterfaceLayer):

    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue" #list of (jid, message) tuples

    def __init__(self):
        super(SendMedia, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()
        self.connected = True
        self.jidAliases = {
            # "NAME": "PHONE@s.whatsapp.net"
        }

    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            phone, filename, mediafiletype = target
            print("\n %s" % phone)
            print("\n %s" % filename)
            print("\n %s" % mediafiletype)
            #self.audio_send(phone, message, mediafiletype)

            if mediafiletype == "image":
                self.image_send(phone, filename)
            elif mediafiletype == "audio":
                self.audio_send(phone, filename)
            elif mediafiletype == "video":
                self.vedio_send(phone, filename)
            else:
                print("Invalid file")


    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            self.lock.release()
            logger.info("Message sent")
            raise KeyboardInterrupt()

        self.lock.release()
    #--------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------image------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------

    def image_send(self, number, path):
        if self.assertConnected():
            jid = self.aliasToJid(number)
            entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath=path)
            successFn = lambda successEntity, originalEntity: self.onRequestUploadResultImage(jid, path, successEntity, originalEntity)
            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)

            self._sendIq(entity, successFn, errorFn)

    def doSendImage(self, filePath, url, mediaType, to, ip = None):
        caption = ""
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, mediaType, ip, to, caption)
        self.toLower(entity)

    def onRequestUploadResultImage(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendImage(filePath, resultRequestUploadIqProtocolEntity.getUrl(), "image", jid,
                             resultRequestUploadIqProtocolEntity.getIp())
        else:
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccessImage, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onUploadSuccessImage(self, filePath, jid, url):
        self.doSendImage(filePath, url, "audio", jid)
    #--------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------audio------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------
    def audio_send(self, number, path):
        if self.assertConnected():
            jid = self.aliasToJid(number)
            entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO, filePath=path)
            successFn = lambda successEntity, originalEntity: self.onRequestUploadResultAudio(jid, path, successEntity, originalEntity)
            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)

            self._sendIq(entity, successFn, errorFn)

    def doSendAudio(self, filePath, url, mediaType, to, ip = None):
        caption = ""
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, mediaType, ip, to, caption)
        self.toLower(entity)

    def onRequestUploadResultAudio(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendAudio(filePath, resultRequestUploadIqProtocolEntity.getUrl(), "audio", jid,
                             resultRequestUploadIqProtocolEntity.getIp())
        else:
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccessAudio, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onUploadSuccessAudio(self, filePath, jid, url):
        self.doSendAudio(filePath, url, "audio", jid)
    #--------------------------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------vidio------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------------------------

    def vedio_send(self, number, path):
        if self.assertConnected():
            jid = self.aliasToJid(number)
            entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO, filePath=path)
            successFn = lambda successEntity, originalEntity: self.onRequestUploadResultVedio(jid, path, successEntity, originalEntity)
            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)

            self._sendIq(entity, successFn, errorFn)

    def doSendVedio(self, filePath, url, mediaType, to, ip = None):
        caption = ""
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, mediaType, ip, to,caption)
        self.toLower(entity)

    def onRequestUploadResultVedio(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendVedio(filePath, resultRequestUploadIqProtocolEntity.getUrl(), "video", jid,
                             resultRequestUploadIqProtocolEntity.getIp())
        else:
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      self.onUploadSuccessVedio, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onUploadSuccessVedio(self, filePath, jid, url):
        self.doSendVedio(filePath, url, "audio", jid)
    #--------------------------------------------------------------------------------------------------------------------------------

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logger.error("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        logger.error("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()

    def assertConnected(self):
        if self.connected:
            return True
        else:
            self.output("Not connected", tag = "Error", prompt = False)
            return False

    def aliasToJid(self, calias):
        for alias, ajid in self.jidAliases.items():
            if calias.lower() == alias.lower():
                return self.normalizeJid(ajid)

        return self.normalizeJid(calias)

    def jidToAlias(self, jid):
        for alias, ajid in self.jidAliases.items():
            if ajid == jid:
                return alias
        return jid

    def normalizeJid(self, number):
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@g.us" % number

        return "%s@s.whatsapp.net" % number
