<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>商品検索結果</v-card-title>
        <v-card-text> 
            <v-row>
                <v-col align="center">
                    <v-img
                        v-if="!isError"
                        :src="path"
                        max-width="400"
                    />
                </v-col>
            </v-row>
            <v-divider />
            <v-simple-table v-if="!isError">
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

            <v-alert 
                v-if="isError"
                icon="mdi-alert"
                type="error"
            >エラーが発生しました。商品が登録されていないか該当する商品が2つ以上ある可能性があります。
            </v-alert>

            <v-divider />
            <v-row class="pt-7"> 
                <v-btn
                    dark
                    color="primary"
                    to="/main/" 
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    最初のページに戻る    
                </v-btn>  
            </v-row>
        </v-card-text>   
    </v-card>
</template>
<script>
export default{
    data: () => ({
        item:{},
        isError:false,
        path:''
    }),
    props:["duct","genre","totalQuery"],
    methods: {
        send_query() {
            const _query = this.totalQuery;
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.NEJI,
                {'genre': this.genre, 'query': _query}
            );
        },
    }, 
    computed:{
        tableData(){
            const _arr = Object.entries(this.item).map(([key, value]) => ({key, value}));
            return _arr
        },
    },
    created(){
        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {
                    console.log(data);
                    this.$set(this, 'item', 'items' in data ? data.items[0] : {});
                    if(!Object.keys(data).includes("items")){
                        this.isError = true;
                    }else{
                        this.isError = false;
                        console.log(this.tableData);
                        let _jan = String(this.tableData[0].value);
                        this.path = require(`@/assets/productsImage/${_jan}.jpg`);
                    }
                }
            )
            this.send_query();
        });
    },
    mounted(){
        this.$emit('add-step', 4);
    }
}
</script>
