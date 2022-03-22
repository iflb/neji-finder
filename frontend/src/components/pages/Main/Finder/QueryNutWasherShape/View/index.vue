<template>
    <v-card class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の形状を選ぶ</v-card-title>
        <v-card-text> 
            <card-button
                v-model="selectedShapeName"
                :headerIsOn="false"
                :inputItems="selectedItems"
                :labelIsOn="true"
                @update-query="makeQuery"
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
        query: {},
        genreEng:'',
        syncStateReceiveRequestId:null,
        selectedShapeName: null,
    }),
    props:["duct","syncId","genre"],
    computed:{
        selectedItems(){
            return this.nut_washer_icons[this.genreEng]
        }
    },
    methods: {
        send_query() {
            if (this.syncId === null) return;
            let _query = {};
            if (this.query) _query = this.query;
            
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId, 'genre': this.genre, 'query': _query},
            );
        },
        unsetGenre(){
            this.query = {};
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {
                    sync_id: this.syncId,
                    query: this.query,
                },
            );
        },
        makeQuery(item){
            let _queryKey = '';
            if(this.genreEng == 'nut'){
                _queryKey = 'ナット形状'
            }else if(this.genreEng == 'washer'){
                _queryKey = '座金形状'
            }

            this.nextPage = true;
            this.query = {};
            this.query[_queryKey] = item.name;
            changeBackgroundColor(item, this.nut_washer_icons[this.genreEng]);

            this.send_query();
        },
        accessNextPage(){
            changeBackgroundColor({ name: '' }, this.nut_washer_icons[this.genreEng]);
            this.$emit( 'emit-query', this.query );
            this.query = {};
            this.$emit( 'emit-component-name', 'query-spec' );
        },
        backToPreviousPage(){
            changeBackgroundColor({ name: '' }, this.nut_washer_icons[this.genreEng]);
            this.query = {};
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
                        this.$set(this, 'query', 'query' in data && Object.keys(data.query).length > 0 ? data.query : {});

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
