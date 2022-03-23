<template>
    <v-card class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>商品検索結果</v-card-title>
        <v-card-text> 
            <v-row>
                <v-col align="center">
                    <v-img
                        :src="path"
                        max-width="400"
                    />
                    <div v-if="this.item" class="text-h6 mt-4">
                        <span v-if="this.item[0]['店舗取り扱い']=='お取り寄せ'">店舗在庫なし</span>
                        <span v-else-if="this.item[0]['店舗取り扱い']=='〇'">店舗在庫あり</span>
                    </div>
                </v-col>
            </v-row>
            <v-row class="pb-3" justify="center">
                <v-col cols="12" md="6">
                    <v-simple-table>
                        <template v-slot:default>
                            <tbody>
                                <tr
                                    v-for="item in tableData"
                                    :key="item.key"
                                >
                                    <td>{{item.key}}</td>
                                    <td>{{item.value}}</td>
                                </tr>
                            </tbody>
                        </template>
                    </v-simple-table>
                </v-col>
            </v-row>
            <!--<v-row class="py-2"> 
                <v-col>
                    <v-dialog
                        v-model="shopArea" 
                        class="py-2"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                color="red lighten-1"
                                dark
                                v-bind="attrs"
                                v-on="on"
                            ><v-icon>mdi-map-marker</v-icon>商品の場所を表示
                            </v-btn>
                        </template>
                        <v-card>
                            <v-card-title>商品マップ</v-card-title>
                            <v-card-text>
                                <v-img
                                    :src="require('@/assets/productsImage/map_example.jpg')"
                                />
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer />
                                <v-btn
                                    color="red lighten-1"
                                    text
                                    @click="shopArea = false"
                                >閉じる
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-col>
            </v-row>-->

            <v-divider/>
            <v-row class="pt-3 pb-0" v-if="itemList.length != 0"> 
                <v-col>
                    <v-btn
                        dark
                        color="indigo darken-1"
                        @click="backToPreviousPage"
                        :width="['md','lg','xl'].includes($vuetify.breakpoint.name) ? '20%' : '60%'" 
                    >
                        <v-icon>mdi-arrow-left</v-icon>
                        前のページに戻る    
                    </v-btn>
                </v-col>  
            </v-row>
            <v-row class="pt-0 mt-0"> 
                <v-col>
                    <v-btn
                        dark
                        color="indigo darken-1"
                        @click="backToFirstPage"
                        :width="['md','lg','xl'].includes($vuetify.breakpoint.name) ? '20%' : '60%'" 
                    >
                        <v-icon>mdi-arrow-left</v-icon>
                        最初のページに戻る    
                    </v-btn>
                </v-col>  
            </v-row>
        </v-card-text>   
    </v-card>
</template>
<script>
export default{
    data: () => ({
        path:'',
        syncStateReceiveRequestId:null,
        shopArea:false
    }),
    props:["item","itemList","duct","syncId"],
    methods:{
        backToPreviousPage(){
            if(this.itemList.length != 1){
                this.$emit( 'emit-component-name', 'result-list' );
            }else{
                this.$emit( 'emit-component-name', 'query-spec' );
            }
        },
        backToFirstPage(){
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_CANCEL,
                {
                    sync_id: this.syncId
                },
            );
            this.$emit( 'initialize-sync' );
            this.$emit( 'emit-genre', "" );
            this.$emit( 'emit-shape-query', {} );
            this.$emit( 'emit-item-list', [] );
            this.$emit( 'emit-item', [] );
            this.$emit( 'emit-component-name', 'start-screen' );
        }
    },
    computed:{
        tableData(){
            const _arr = Object.entries(this.item[0]).map(([key, value]) => ({key, value}));
            let _arr2 = _arr.filter(item => { 
                if(item.key == "画像" || item.value == null){
                    return false
                }else if(!isNaN(item.value) || typeof item.value === 'string'){
                    return true
                }else{
                    return false
                }
            });
            return _arr2
        },
    },
    created(){
        this.$vuetify.goTo(0);
        let _jan = String(this.tableData[0].value);
        try{
            this.path = require(`../../../../../../assets/productsImage/${_jan}.jpg`);
        }catch{
            this.path = require(`../../../../../../assets/productsImage/no_image.jpg`);
        }

        const storagedItemsKey = Object.keys(window.localStorage).filter(key => key.includes('neji-product'));
        const storagedItemsString = storagedItemsKey.map((key) => window.localStorage[key]);
        let storagedItemsJSON = [];
        for(let item of storagedItemsString){
            storagedItemsJSON.push(JSON.parse(item));
        }
        if (!storagedItemsJSON.map(item => item.jan).includes(this.item[0]["JANコード"])){
            let _index = 0;
            const storagedItemsLength = storagedItemsKey.length;
            if(storagedItemsLength != 0) _index = storagedItemsLength;
            const _itemStoraging = {
                name: this.item[0]["品名"] + `(サイズ：${this.item[0]["サイズ"]}, 構成数:${this.item[0]["構成数"]})`,
                src: this.path,
                backgroundColor: "#FFFFFF",
                index: _index,
                jan: this.item[0]["JANコード"],
                data: this.item[0]
            }
            window.localStorage.setItem('neji-product' + String(_index), JSON.stringify(_itemStoraging));
        }

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
    }
}
</script>
