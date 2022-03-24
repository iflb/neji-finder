
<template>
    <v-card class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>該当商品一覧：{{itemQuantity}}個</v-card-title>
        <v-card-text> 
            <card-button 
                v-model="selectedItemName"
                :headerIsOn="false"
                :inputItems="selectableItems"
                :labelIsOn="true"
                @update="accessNextPage"
            />
            <v-divider class="pt-3"/>
            <page-transition-button 
                :nextIsNecessary="false"
                @click-back="removeQueryFixedParameter"
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
        selectedItemName: null,
        pickedItem:[],
        itemQuantity:0,
        syncStateReceiveRequestId:null,
    }),
    props:["itemList","duct","syncId","genre","totalQuery"],
    methods: {
        removeQueryFixedParameter(){
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {
                    sync_id: this.syncId,
                    genre: this.genre,
                    query: this.totalQuery,
                },
            );
        },
        accessNextPage(){
            let itemIdx = this.selectableItems.findIndex(item => (item.name === this.selectedItemName));
            this.$emit( 'emit-item', [this.itemList[itemIdx]] );
            this.$emit( 'emit-component-name', 'result' );
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        },
        backToPreviousPage(){
            this.$emit( 'emit-component-name', 'query-spec' );
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        }
    }, 
    computed:{
        selectableItems(){
            let _arr = [];
            let _ind = 0;
            this.itemList.forEach((item) =>{
                let _path = "";
                const _jan = String(item["JANコード"]);
                try{
                    _path = require(`../../../../../../assets/productsImage/${_jan}.jpg`);
                }catch{
                    _path = require(`../../../../../../assets/productsImage/no_image.jpg`);
                }
                _arr.push({
                    name: item["品名"] + `(サイズ：${item["サイズ"]}, 構成数:${item["構成数"]})`,
                    src: _path,
                    backgroundColor: "#FFFFFF",
                    index: _ind,
                    jan: _jan
                })
                _ind++;
            });
            return _arr        
        },
    },
    created(){
        this.itemQuantity = this.itemList.length;
        this.syncStateReceiveRequestId = this.duct.nextRid();
        this.$emit(
            'register-sync-state-receive-handler',
            {
                rid: this.syncStateReceiveRequestId,
                handler: (rid, eid, data) => {
                    if (!Object.keys(data).includes('query_fixed')) {
                        this.backToPreviousPage();
                    }
                }
            },
        );
    },
    mounted(){
        this.$emit('add-step', 4);
    },
    destroyed(){
        this.$emit(
            'unregister-sync-state-receive-handler',
            { rid: this.syncStateReceiveRequestId },
        );
    },
}
</script>
