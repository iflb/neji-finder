<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>おねじの形状を選ぶ</v-card-title>
        <v-card-text> 
            <v-container>
                <card-button 
                    :headerIsOn="true"
                    headerTitle="頭部の形状"
                    :inputItems="bolt_icons.head"
                    @update-query="makeQuery"
                    :labelIsOn="true"
                />
            </v-container>

            <v-slide-y-transition>
                <v-container v-if="isPicked.head">
                    <v-divider />
                    <carousel-button
                       :headerIsOn="true"
                       headerTitle="おねじ先端の形状"
                       :inputItems="selectableTip"
                       @update-query="makeQuery"
                    />
                </v-container>
            </v-slide-y-transition>
            <v-slide-y-transition>
                <v-container v-if="isPicked.tip">   
                    <v-divider />
                    <carousel-button
                        :headerIsOn="true"
                        headerTitle="頭部穴の形状"
                        :inputItems="selectableHoleShape"
                        @update-query="makeQuery"
                    />
                </v-container>
            </v-slide-y-transition>

            <v-divider />
            <v-row class="py-5"> 
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
import CardButton from '../../CardButton'
import CarouselButton from '../../CarouselButton'
import { bolt_icons } from '../../shape_profile.js'
function changeBackgroundColor(pickedItem, icons){
    for (let item of icons){
        if(pickedItem.name !== item.name){
            item.backgroundColor = "#FFFFFF";
        }
    }
    pickedItem.backgroundColor = "#FFCA28"
}
export default{
    components:{
        CardButton,
        CarouselButton
    },
    data: () => ({
        bolt_icons,
        isPicked: { head:false, tip:false, hole_shape:false },
        pickedTip:[],
        pickedHoleShape:[],
        query: {},
        shape: {},
    }),
    props:["duct","genre"],
    computed:{
        selectableTip(){
            let _arr = [];
            this.bolt_icons.tip.forEach((item) => {
                if(this.pickedTip.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableHoleShape(){
            let _arr = [];
            this.bolt_icons.hole_shape.forEach((item) => {
                if(this.pickedHoleShape.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
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
            if(this.bolt_icons.head.includes(item)){
                this.query = {};
                for (let key in this.isPicked){
                    this.isPicked[key] = false;
                }
                this.query["頭部"] = item.name;
                this.isPicked.head = true;
                changeBackgroundColor(item, this.bolt_icons.hole_shape);
                changeBackgroundColor(item, this.bolt_icons.tip);
                changeBackgroundColor(item, this.bolt_icons.head);
                this.send_query();
            }else if(this.bolt_icons.tip.includes(item)){
                this.query["おねじ先端"] = item.name;
                this.isPicked.tip = true;
                changeBackgroundColor(item, this.bolt_icons.tip);

                this.send_query();
            }else if(this.bolt_icons.hole_shape.includes(item)){
                this.query["頭部穴形状"] = item.name;
                this.isPicked.hole_shape = true;
                changeBackgroundColor(item, this.bolt_icons.hole_shape);
                this.send_query();
            }
        },
        accessNextPage(){
            changeBackgroundColor({ name: '' }, this.bolt_icons.hole_shape);
            changeBackgroundColor({ name: '' }, this.bolt_icons.tip);
            changeBackgroundColor({ name: '' }, this.bolt_icons.head);
            this.$emit( 'emit-shape-query', this.query );
            this.$emit( 'emit-component-name', 'query-spec' );
        },
        backToPreviousPage(){
            changeBackgroundColor({ name: '' }, this.bolt_icons.hole_shape);
            changeBackgroundColor({ name: '' }, this.bolt_icons.tip);
            changeBackgroundColor({ name: '' }, this.bolt_icons.head);
            this.query = {};
            this.$emit( 'emit-shape-query', this.query );
            this.$emit( 'emit-component-name', 'query-genre' );
        }
    }, 
    created(){
        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {
                    this.$set(this, 'query', 'query' in data && Object.keys(data.query).length > 0 ? data.query : {});
                    this.$set(this, 'shape', 'shape' in data ? data.shape : '');

                    if(!Object.keys(this.query).includes("おねじ先端")){
                        this.pickedTip = this.shape["おねじ先端"];
                    }
                    if(!Object.keys(this.query).includes("頭部穴形状")){
                        this.pickedHoleShape = this.shape["頭部穴形状"];
                    }
                    if(Object.keys(this.query).length === 3){
                         this.accessNextPage();
                    } else {
                        this.$nextTick(() => {
                            this.$vuetify.goTo(document.body.scrollHeight);
                        });
                    }
                }
            );
            this.send_query();
        });
    },
    mounted(){
        this.$emit('add-step', 2);
    }
}
</script>

