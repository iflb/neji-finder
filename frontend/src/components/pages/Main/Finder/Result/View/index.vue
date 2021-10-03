<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>商品検索結果</v-card-title>
        <v-card-text> 
            <v-row>
                <v-col align="center">
                    <v-img
                        :src="path"
                        max-width="400"
                    />
                </v-col>
            </v-row>
            <v-divider />
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

            <v-divider />
            <v-row class="pt-7"> 
                <v-btn
                    dark
                    color="primary"
                    @click="backToPreviousPage"
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    前のページに戻る    
                </v-btn>  
            </v-row>
            <v-row class="pt-7"> 
                <v-btn
                    dark
                    color="primary"
                    @click="backToFirstPage"
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
        path:''
    }),
    props:["item","itemList"],
    methods:{
        backToPreviousPage(){
            if(this.itemList.length != 0){
                this.$emit( 'emit-component-name', 'result-list' );
            }else{
                this.$emit( 'emit-component-name', 'query-spec' );
            }
        },
        backToFirstPage(){
            this.$emit( 'emit-genre', "" );
            this.$emit( 'emit-shape-query', {} );
            this.$emit( 'emit-item-list', [] );
            this.$emit( 'emit-item', [] );
            this.$emit( 'emit-component-name', 'start' );
        }
    },
    computed:{
        tableData(){
            const _arr = Object.entries(this.item[0]).map(([key, value]) => ({key, value}));
            let _arr2 = _arr.filter(item => { 
                if(!isNaN(item.value) || typeof item.value === 'string'){
                    return true
                }else{
                    return false
                }
            });
            return _arr2
        },
    },
    created(){
        console.log(this.tableData);
        let _jan = String(this.tableData[0].value);
        try{
            this.path = require(`@/assets/productsImage/${_jan}.jpg`);
        }catch{
            this.path = require(`@/assets/productsImage/no_image.jpg`);
        }
    },
    mounted(){
        this.$emit('add-step', 4);
    }
}
</script>
