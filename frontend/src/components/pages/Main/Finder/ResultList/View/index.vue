
<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>該当商品一覧：{{itemQuantity}}個</v-card-title>
        <v-card-text> 
            <card-button 
                :headerIsOn="false"
                :inputItems="selectableItems"
                :labelIsOn="true"
                @update-query="accessNextPage"
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
        pickedItem:[],
        itemQuantity:0
    }),
    props:["itemList"],
    methods: {
        accessNextPage(item){
            this.$emit( 'emit-item', [this.itemList[item.index]] );
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
    watch:{
    },
    computed:{
        selectableItems(){
            let _arr = [];
            let _ind = 0;
            this.itemList.forEach((item) =>{
                let _path = "";
                let _jan = String(item["JANコード"]);
                try{
                    _path = require(`@/assets/productsImage/${_jan}.jpg`);
                }catch{
                    _path = require(`@/assets/productsImage/no_image.jpg`);
                }
                _arr.push({
                    name: item["品名"] + `(サイズ：${item["サイズ"]}, 構成数:${item["構成数"]})`,
                    src: _path,
                    backgroundColor: "#FFFFFF",
                    index: _ind,
                    jan: item["JANコード"]
                })
                _ind++;
            });
            return _arr        
        },
    },
    created(){
        this.itemQuantity = this.itemList.length;
    },
    mounted(){
        this.$emit('add-step', 4);
    }
}
</script>
