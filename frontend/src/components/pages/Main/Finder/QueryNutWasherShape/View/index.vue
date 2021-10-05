<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の形状を選ぶ</v-card-title>
        <v-card-text> 
            <v-container>
                <card-button
                    :headerIsOn="false"
                    :inputItems="selectedItems"
                    :labelIsOn="true"
                    @update-query="makeQuery"
                />
            </v-container>
            <v-divider />
            <v-row class="pt-7"> 
                <v-btn
                    dark
                    color="primary"
                    @click="backToPreviousPage"
                >
                    <v-icon>mdi-arrow-left</v-icon>
                    戻る    
                </v-btn>  
            </v-row>
        </v-card-text>   
    </v-card>
</template>
<script>
import { nut_washer_icons } from '../../shape_profile.js'
import CardButton from '../../CardButton' 
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
        CardButton
    },
    data: () => ({
        nut_washer_icons,
        isPicked: false,
        query: {},
        shape: {},
    }),
    props:["duct","genre"],
    computed:{
        selectedItems(){
            if (this.genre == "めねじ"){
                return this.nut_washer_icons.nut
            }else if(this.genre == "座金"){
                return this.nut_washer_icons.washer
            }else{
                return 0
            }
        }
    },
    methods: {
        send_query() {
            let _query = '';
            if (this.query){
                _query = this.query;
            }
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.NEJI,
                {'genre': this.genre, 'query': _query}
            );
        },
        makeQuery(item){
            if(this.nut_washer_icons.nut.includes(item)){
                this.query = {};
                this.query["ナット形状"] = item.name;
                this.isPicked = true;
                changeBackgroundColor(item, this.nut_washer_icons.nut);
            }else if(this.nut_washer_icons.washer.includes(item)){
                this.query = {};
                this.query["座金形状"] = item.name;
                this.isPicked = true;
                changeBackgroundColor(item, this.nut_washer_icons.washer);
            }
            this.send_query();
        },
        accessNextPage(){
            changeBackgroundColor({ name: '' }, this.nut_washer_icons.nut);
            changeBackgroundColor({ name: '' }, this.nut_washer_icons.washer);
            this.$emit( 'emit-shape-query', this.query );
            this.query = {};
            this.$emit( 'emit-component-name', 'query-spec' );
        },
        backToPreviousPage(){
            changeBackgroundColor({ name: '' }, this.nut_washer_icons.nut);
            changeBackgroundColor({ name: '' }, this.nut_washer_icons.washer);
            this.query = {};
            this.$emit( 'emit-component-name', 'query-genre' );
        }
    }, 
    created(){
        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {
                    console.log(data);
                    this.$set(this, 'query', 'query' in data && Object.keys(data.query).length > 0 ? data.query : {});
                    this.$set(this, 'shape', 'shape' in data ? data.shape : '');
                    if(Object.keys(this.query).length === 1){
                         this.accessNextPage();
                    } else {
                        this.$nextTick(() => {
                            this.$vuetify.goTo(document.body.scrollHeight);
                        });
                    }
                }
            )
            this.send_query();
        });
    },
    mounted(){
        this.$emit('add-step', 2);
    }
}
</script>
