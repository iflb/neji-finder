<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title color="primary">ジャンルを決定する</v-card-title>
        <v-card-text> 
            <card-button
                v-model="selectedGenreName"
                :input-items="selectableGenreIcons"
                :label-is-on="true"
            />
            <v-divider class="pt-3"/>
            <page-transition-button 
                :next-is-necessary="false"
                @click-back="backToPreviousPage"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import { Duct } from '@iflb/ducts-client'
import CardButton from '../../CardButton'
import PageTransitionButton from '../../PageTransitionButton'
const genreIcons = [
    { 
        name: "おねじ", 
        src: require("../../../../../../assets/icons/1_bolt.jpg"), 
    },
    { 
        name: "めねじ", 
        src: require("../../../../../../assets/icons/2_nut.jpg"), 
    },
    { 
        name: "座金", 
        src: require("../../../../../../assets/icons/3_washer.jpg"), 
    },
];

export default{
    watch: {
        selectedGenreName() {
            this.sendQuery();
        },
    },
    components:{
        CardButton,
        PageTransitionButton
    },
    data: () => ({
        syncStateReceiveRequestId: null,
        selectedGenreName: null,
    }),

    props: {
        duct: { type: Duct },
        syncId: { type: String },
    },

    computed: {
        selectableGenreIcons() { return genreIcons },
    },
    methods: {
        sendQuery(){
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId,'genre': this.selectedGenreName, 'query': {}},
            );
        },
        accessNextPage(genreName){
            this.$emit( 'emit-genre', genreName );
            switch (genreName) {
                case 'めねじ':
                    this.$emit('emit-component-name', 'query-nut-washer-shape');
                    break;
                case '座金':
                    this.$emit('emit-component-name', 'query-nut-washer-shape');
                    break;
                case 'おねじ':
                    this.$emit('emit-component-name', 'query-bolt-shape');
                    break;
            }
        },
        backToPreviousPage(){
            this.$emit( 'emit-component-name', 'start-screen' );
        },
    }, 
    created() {
        this.syncStateReceiveRequestId = this.duct.nextRid();
        this.$emit( 'emit-footer-component-name', 'ask-for-image-search-support' );
        this.$emit(
            'register-sync-state-receive-handler',
            {
                rid: this.syncStateReceiveRequestId,
                handler: (rid, eid, data) => {
                    let dataKeys = Object.keys(data);
                    if (dataKeys.includes('genre')) {
                        this.$nextTick(() => {
                            this.accessNextPage(data.genre);
                        });
                    }
                },
            }
        );
    },
    destroyed() {
        this.$emit(
            'unregister-sync-state-receive-handler',
            { rid: this.syncStateReceiveRequestId },
        );
    },
    mounted(){
        this.$emit('add-step',1)
    }
}
</script>
<style>
.imgOpacity{
    opacity: 0.75
}
</style>

