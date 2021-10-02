
<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>該当商品一覧：{{itemQuantity}}個</v-card-title>
        <v-card-text> 
            <card-button 
                :headerIsOn="false"
                headerTitle="材質"
                :inputItems="selectableItems"
                :labelIsOn="true"
                @update-query="accessNextPage"
            />
            <v-row class="pt-5"> 
                <v-btn
                    dark
                    color="primary"
                    to="/main/finder/query-genre" 
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    戻る    
                </v-btn>  
                <v-spacer />
            </v-row>
        </v-card-text>   
    </v-card>
</template>
<script>
import CardButton from '../../CardButton'
export default{
    components:{
        CardButton,
    },
    data: () => ({
        pickedItem:[],
        itemQuantity:0
    }),
    props:["items"],
    methods: {
        accessNextPage(item){
            this.$router.push({
                name: "FinderResult",
                params:{ 'item': [this.items[item.index]] }
            });
        }
    }, 
    watch:{
    },
    computed:{
        selectableItems(){
            let _arr = [];
            let _ind = 0;
            this.items.forEach((item) =>{
                let _path = "";
                let _jan = String(item["JANコード"]);
                try{
                    _path = require(`@/assets/productsImage/${_jan}.jpg`);
                }catch{
                    _path = require(`@/assets/productsImage/no_image.jpg`);
                }
                _arr.push({
                    name: item["品名"] + `(${item["JANコード"]})`,
                    src: _path,
                    backgroundColor: "#FFFFFF",
                    index: _ind
                })
                _ind++;
            });
            return _arr        
        },
    },
    created(){
        console.log(this.items);
        console.log(this.selectableItems);
        this.itemQuantity = this.items.length;
    },
    mounted(){
        this.$emit('add-step', 4);
    }
}
</script>
