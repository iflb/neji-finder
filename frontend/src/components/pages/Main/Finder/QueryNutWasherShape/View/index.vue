<template>
    <v-card class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の形状を選ぶ</v-card-title>
        <v-card-text> 
            <card-button
                v-model="selectedShapeName"
                :headerIsOn="false"
                :inputItems="selectedItems"
                :labelIsOn="true"
                @update="send_query"
            />
            <v-divider class="pt-3"/>
            <page-transition-button 
                :nextIsNecessary="false"
                @click-back="unsetGenre"
            />
        </v-card-text>   
    </v-card>
</template>
<script>
import { nut_washer_icons } from '../../shape_profile.js'
import CardButton from '../../CardButton' 
import PageTransitionButton from '../../PageTransitionButton'
function changeBackgroundColor(pickedItem, nut_washer_icons){
    for (let item of nut_washer_icons){
        if(pickedItem.name !== item.name){
            item.backgroundColor = "#FFFFFF";
        }
    }
    pickedItem.backgroundColor = "#FFCA28"
}
export default{
    components:{
        CardButton,
        PageTransitionButton
    },
    data: () => ({
        nut_washer_icons,
        nextPage:true,
        genreEng:'',
        syncStateReceiveRequestId:null,
        selectedShapeName: null,
    }),
    props:["duct","syncId","genre"],
    computed:{
        selectedItems(){
            return this.nut_washer_icons[this.genreEng]
        },
        query() {
            let query = {};
            let queryKey = null;
            switch (this.genreEng) {
                case 'nut':
                    queryKey = 'ナット形状';
                    break;
                case 'washer':
                    queryKey = '座金形状';
                    break;
            }
            if (this.selectedShapeName !== null) {
                query[queryKey] = this.selectedShapeName;
            }
            return query;
        },
    },
    methods: {
        send_query() {
            if (this.syncId === null) return;
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId, 'genre': this.genre, 'query': this.query},
            );
        },
        unsetGenre(){
            this.selectedShapeName = null;
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {
                    sync_id: this.syncId,
                },
            );
        },
        accessNextPage(){
            changeBackgroundColor({ name: '' }, this.nut_washer_icons[this.genreEng]);
            this.$emit( 'emit-query', this.query );
            this.$emit( 'emit-component-name', 'query-spec' );
        },
        backToPreviousPage(){
            changeBackgroundColor({ name: '' }, this.nut_washer_icons[this.genreEng]);
            this.$emit( 'emit-component-name', 'query-genre' );
        }
    }, 
    created(){
        this.nextPage = false;

        if (this.genre == "めねじ"){
            this.genreEng = 'nut';
        }else if(this.genre == "座金"){
            this.genreEng = 'washer';
        }

        this.syncStateReceiveRequestId = this.duct.nextRid();
        this.$emit(
            'register-sync-state-receive-handler',
            {
                rid: this.syncStateReceiveRequestId,
                handler: (rid, eid, data) => {
                    if(!Object.keys(data).includes('genre')){
                        this.backToPreviousPage();
                    }else{
                        if(Object.keys(data).includes('spec')){
                            this.accessNextPage();
                        }else{
                            this.$nextTick(() => {
                                this.$vuetify.goTo(document.body.scrollHeight);
                            });
                        }
                    }
                },
            }
        );
    },
    mounted(){
        this.$emit('add-step', 2);
    },
    destroyed(){
        this.$emit(
            'unregister-sync-state-receive-handler',
            { rid: this.syncStateReceiveRequestId },
        );
    },
}
</script>
