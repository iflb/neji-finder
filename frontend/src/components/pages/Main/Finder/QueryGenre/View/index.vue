<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title color="primary">ジャンルを決定する</v-card-title>
        <v-card-text> 
            <card-button
                v-model="selectedGenre"
                :headerIsOn="false"
                :inputItems="icons"
                @update="chooseGenre"
                :labelIsOn="true"
            />
            <v-divider class="pt-3"/>
            <page-transition-button 
                :nextIsNecessary="false"
                @click-back="backToPreviousPage"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import CardButton from '../../CardButton'
import PageTransitionButton from '../../PageTransitionButton'
export default{
    components:{
        CardButton,
        PageTransitionButton
    },
    data: () => ({
        icons: [
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
        ],
        syncStateReceiveRequestId: null,
        selectedGenre: null,
    }),
    props:["duct","syncId"],
    methods: {
        chooseGenre(){
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId,'genre': this.selectedGenre, 'query': {}},
            );
            this.accessNextPage(this.selectedGenre);
        },
        accessNextPage(genre){
            this.$emit( 'emit-genre', genre );
            if(["めねじ","座金"].includes(genre)){
                this.$emit( 'emit-component-name', 'query-nut-washer-shape' );
            }else{
                this.$emit( 'emit-component-name', 'query-bolt-shape' );
            }
        },
        backToPreviousPage(){
            this.$emit( 'emit-component-name', 'start-screen' );
        },
        emitFooterComponentName(){
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
                        let foundGenre = this.icons.map(icon => icon.name).find(iconName => (iconName === data.genre));
                        if (foundGenre) {
                            this.$nextTick(() => {
                                this.accessNextPage(foundGenre);
                            });
                        }
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

