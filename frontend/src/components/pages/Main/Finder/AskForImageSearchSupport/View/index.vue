<template>
    <v-card
        tile
        id="base-container"
    >
        <v-card-actions class="pa-0">
            <template v-if="!minimized">
                <template v-if="cameraEnabled">
                    <v-btn
                        text
                        @click="disableCamera"
                    >
                        <v-icon>mdi-camera-off</v-icon>カメラ停止
                    </v-btn>
                    <v-btn
                        text
                        v-if="captureStarted"
                        @click="stopCapture"
                    >
                        <v-icon>mdi-image-off</v-icon>キャプチャ停止
                    </v-btn>
                    <v-btn
                        text
                        v-else
                        :disabled="!captureEnabled"
                        @click="startCapture"
                    >
                        <v-icon>mdi-image-plus</v-icon>キャプチャ開始
                    </v-btn>
                </template>
                <template v-else>
                    <v-btn
                        text
                        @click="enableCamera"
                    >
                        <v-icon>mdi-camera</v-icon>カメラ起動
                    </v-btn>
                </template>
            </template>
            <v-spacer />
            <v-btn
                text
                v-if="minimized"
                @click="maximize"
            >
                <v-icon>mdi-window-maximize</v-icon>
            </v-btn>
            <v-btn
                text
                v-else
                @click="minimize"
            >
                <v-icon>mdi-window-minimize</v-icon>
            </v-btn>
        </v-card-actions>
        <v-card-text
            id="media-container"
            ref="mediaContainer"
            class="pa-0"
            v-show="!minimized"
        >
            <video
                id="video"
                ref="video"
                v-show="cameraEnabled"
                autoplay muted playsinline
            />
            <div
                id="capture-history"
                ref="captureHistory"
            />
        </v-card-text>
    </v-card>
</template>

<style scoped>
#base-container {
    width: 100%;
}

div#media-container {
    display: flex;
    flex-direction: row;
    background-color: rgb(0,0,0);
    overflow-x: auto;
}

div#capture-history {
    display: flex;
    flex-direction: row;
}

video#video {
    display: inline-block;
}
</style>

<script>
import { Duct } from '@iflb/ducts-client'

const constraintsForCamera = {
    audio: false,
    video: {
        facingMode: 'environment',
    }
};
const autoCaptureIntervalTimeMsec = 500;
const commonMediaElementHeight = '30vh';
const commonMediaElementMaxHeight = '300px';
const canvasBlobOutputQualityFactor = 0.95;

export default {
    watch: {
        syncId: {
            handler(newSyncId) {
                if (newSyncId !== null) {
                    this.duct.send(
                        this.duct.nextRid(), 
                        this.duct.EVENT.SYNC_IMAGE_RECEIVE,
                        { sync_id: newSyncId },
                    );
                }
            },
            immediate: true,
        },
    },

    props: {
        syncId: { type: String },
        duct: { type: Duct },
    },

    data: () => ({
        minimized: false,
        mediaContainerElement: null,
        videoElement: null,
        videoStream: null,
        captureEnabled: true,
        captureCameraIntervalId: null,
        captureHistoryElement: null,
        resizeObserver: null,
        videoElementViewPortInOrOutObserver: null,
    }),

    computed: {
        cameraEnabled() {
            return (this.videoStream !== null);
        },

        captureStarted() {
            return (this.captureCameraIntervalId !== null);
        },

        videoStreamTracks() {
            if (this.videoStream === null) return null;
            return this.videoStream.getTracks();
        },

        videoStreamMainTrack() {
            if (this.videoStreamTracks === null) return null;
            return this.videoStreamTracks[0];
        },
    },

    methods: {
        async enableCamera() {
            try {
                this.videoStream = await navigator.mediaDevices.getUserMedia(constraintsForCamera)
            } catch(error) {
                if (error.name === 'NotAllowedError') {
                    throw new Error('カメラへのアクセスが拒否されました(' + error.message + ')');
                } else if (error.name === 'NotFoundError') {
                    throw new Error('カメラデバイスが見つかりませんでした(' + error.message + ')');
                } else {
                    throw new Error('カメラへのアクセス中に予期せぬエラーが発生しました(' + error.message + ')');
                }
            }
            this.videoElement.srcObject = this.videoStream;
        },

        disableCamera() {
            for (let videoStreamTrack of this.videoStreamTracks) {
                videoStreamTrack.stop();
            }
            this.videoStream = null;
        },

        startCapture() {
            let videoStreamTrackSettings = this.videoStreamMainTrack.getSettings();
            this.captureCameraIntervalId = window.setInterval(
                () => {
                    let canvasElement = document.createElement('canvas');
                    canvasElement.width = videoStreamTrackSettings.width;
                    canvasElement.height = videoStreamTrackSettings.height;
                    canvasElement.style.height = commonMediaElementHeight;
                    canvasElement.style.maxHeight = commonMediaElementMaxHeight;
                    let canvasContext = canvasElement.getContext('2d');
                    canvasContext.drawImage(this.videoElement, 0, 0, videoStreamTrackSettings.width, videoStreamTrackSettings.height);
                    canvasElement.toBlob(
                        async (blob) => {
                            let buffer = await blob.arrayBuffer();
                            this.duct.send(
                                this.duct.nextRid(), 
                                this.duct.EVENT.SYNC_IMAGE_ADD,
                                { 'sync_id': this.syncId, 'buf': buffer },
                            );
                        },
                        'image/jpeg',
                        canvasBlobOutputQualityFactor,
                    );
                },
                autoCaptureIntervalTimeMsec,
            );
        },

        stopCapture() {
            window.clearInterval(this.captureCameraIntervalId);
            this.captureCameraIntervalId = null;
        },

        minimize() {
            this.minimized = true;
        },

        maximize() {
            this.minimized = false;
        },

        onVideoElementViewPortInOrOut([ intersectionObserverEntry ]) {
            if (intersectionObserverEntry.isIntersecting) {
                this.captureEnabled = true;
            } else {
                if (this.captureStarted) {
                    this.stopCapture();
                }
                this.captureEnabled = false;
            }
        },
    },

    created() {
        this.$emit(
            'register-sync-image-receive-handler',
            async (rid, eid, data) => {
                let dataKeys = Object.keys(data);
                if (dataKeys.includes('error')) {
                    console.log(data['error']);
                } else {
                    if (dataKeys.includes('content')) {
                        let captureImageBlob = new Blob([ data.content ], { type: "image/jpeg" });
                        var fileReader = new FileReader();
                        fileReader.onloadend = async (event) => {
                            let imageElement = document.createElement('img');
                            imageElement.src = event.target.result;
                            imageElement.style.height = commonMediaElementHeight;
                            imageElement.style.maxHeight = commonMediaElementMaxHeight;
                            if (dataKeys.includes('score')) {
                                let scoreInfoMessage = 'score: ' + String(data['score']);
                                imageElement.alt = scoreInfoMessage;
                                imageElement.title = scoreInfoMessage;
                            }
                            this.captureHistoryElement.insertBefore(imageElement, this.captureHistoryElement.firstChild);
                        }
                        fileReader.readAsDataURL(captureImageBlob);
                    }
                }
            },
        );
    },

    destroyed() {
        this.$emit('unregister-sync-image-entry-handler');
    },

    mounted() {
        this.mediaContainerElement = this.$refs.mediaContainer;
        this.videoElement = this.$refs.video;
        this.videoElement.style.height = commonMediaElementHeight;
        this.videoElement.style.maxHeight = commonMediaElementMaxHeight;
        this.captureHistoryElement = this.$refs.captureHistory;
        this.videoElementViewPortInOrOutObserver = new IntersectionObserver(
            this.onVideoElementViewPortInOrOut,
            {
                root: this.mediaContainerElement,
                threshold: 1.0,
            }
        );
        this.videoElementViewPortInOrOutObserver.observe(this.videoElement);
        this.resizeObserver = new ResizeObserver(
            resizeObserverEntries => {
                this.$emit('update-height', resizeObserverEntries[0].borderBoxSize[0].blockSize);
            },
        );
        this.resizeObserver.observe(this.$el);
    },

    beforeDestroy() {
        this.resizeObserver.disconnect();
        this.videoElementViewPortInOrOutObserver.disconnect();
        if (this.captureStarted) {
            this.stopCapture();
        }
        if (this.cameraEnabled) {
            this.disableCamera();
        }
    },
}
</script>