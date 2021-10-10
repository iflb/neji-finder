<template>
    <v-card tile class="pa-1 ma-1" flat color="grey lighten-3">
        <v-card-title>{{genre}}の規格を選ぶ</v-card-title>
        <v-card-text> 
            <v-row v-if="itemQuantity != 0">
                <v-col>
                    <span class="text-body-1">該当商品数：{{itemQuantity}}個</span>
                </v-col>
            </v-row>
            <v-row v-else>
                <v-col>
                    <span class="text-body-1">該当件数が多すぎます。絞り込んでください</span>
                </v-col>
            </v-row>
            <page-transition-button 
                :nextIsNecessary="true"
                :buttonDisabled="buttonDisabled"
                @click-back="backToPreviousPage"
                @click-next="accessNextPage"
            />
            <v-row>
                <v-col>
                    <v-btn
                        color="red darken-1"
                        dark
                        @click="resetQuery"
                    >規格をリセットする
                    </v-btn>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" md="4">
                    <carousel-button
                        :headerIsOn="true"
                        headerTitle="中分類"
                        :inputItems="selectableMiddleClassification"
                        @update-query="makeQuery"
                        :labelIsOn="true"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        :headerIsOn="true"
                        headerTitle="材質"
                        :inputItems="selectableMaterial"
                        @update-query="makeQuery"
                        :labelIsOn="false"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        :headerIsOn="true"
                        headerTitle="表面処理"
                        :inputItems="selectableSurface"
                        @update-query="makeQuery"
                        :labelIsOn="false"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        :headerIsOn="true"
                        headerTitle="構成数クラス"
                        :inputItems="selectableAmount"
                        @update-query="makeQuery"
                        :labelIsOn="false"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <drop-down-menu
                        headerTitle="呼び径"
                        :imageSource="nominal.image"
                        :model="nominal.model"
                        :inputItems="selectableNominal"
                        @update-query="makeQuery"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4" v-if="outer.isNecessary">
                    <drop-down-menu
                        v-if="outer.isNecessary"
                        headerTitle="外径・幅"
                        :imageSource="outer.image"
                        :model="outer.model"
                        :inputItems="selectableOuter"
                        @update-query="makeQuery"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <drop-down-menu
                        v-if="thickness.isNecessary"
                        headerTitle="長さ・厚さ"
                        :imageSource="thickness.image"
                        :model="thickness.model"
                        :inputItems="selectableThickness"
                        @update-query="makeQuery"
                        class="mb-6"
                    />
                </v-col>
            </v-row>
            <v-divider />
            <v-row v-if="itemQuantity != 0" class="pt-3">
                <v-col>
                    <span class="text-body-1">該当商品数：{{itemQuantity}}個</span>
                </v-col>
            </v-row>
            <v-row v-else class="pt-3">
                <v-col>
                    <span class="text-body-1">該当件数が多すぎます。絞り込んでください</span>
                </v-col>
            </v-row>
            <page-transition-button 
                :nextIsNecessary="true"
                :buttonDisabled="buttonDisabled"
                @click-back="backToPreviousPage"
                @click-next="accessNextPage"
            />
        </v-card-text>   
    </v-card>
</template>
<script>
import { icons } from '../../spec_profile.js'
import CardButton from '../../CardButton'
import CarouselButton from '../../CarouselButton'
import DropDownMenu from '../../DropDownMenu'
import PageTransitionButton from '../../PageTransitionButton'
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
        DropDownMenu,
        CarouselButton,
        PageTransitionButton
    },
    data: () => ({
        icons,
        query:{},
        specQuery:{}, 
        snackbar:false,
        initialSpec:{
            "呼び径": [],
            "表面処理": [],
            "構成数クラス": [],
            "中分類": [],
            "材質": [],
            "外径か幅": [],
            "長さか厚み": [],
        },
        nominal:{
            model:"",
            image:"",
        },
        outer:{
            isNecessary:true,
            model:"",
            image:"",
        },
        thickness:{
            isNecessary:true,
            model:"",
            image:"",
        },
        carouselAndCard:{
            middle_classification: '中分類',
            material: '材質',
            surface: '表面処理',
            amount: '構成数クラス',
        },
        pickedMiddleClassification:[],
        pickedMaterial:[],
        pickedSurface:[],
        pickedAmount:[],
        pickedNominal:[],
        pickedOuter:[],
        pickedThickness:[],
        itemQuantity:0,
        buttonDisabled:true,
        currentItems:[],
        data:{}
    }),
    props:["duct","genre","shapeQuery", "totalQuery"],
    methods: {
        send_query() {
            const _query = {}
            Object.assign(_query, this.shapeQuery,this.specQuery);
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.NEJI,
                {'genre': this.genre, 'query': _query}
            );
        },
        makeQuery(item){
            if(this.icons.middle_classification.includes(item)){
                this.specQuery["中分類"] = item.name;
                changeBackgroundColor(item, this.icons.middle_classification);
            }else if(this.icons.material.includes(item)){
                this.specQuery["材質"] = item.name;
                changeBackgroundColor(item, this.icons.material);
            }else if(this.icons.surface.includes(item)){
                this.specQuery["表面処理"] = item.name;
                changeBackgroundColor(item, this.icons.surface);
            }else if(this.icons.amount.includes(item)){
                this.specQuery["構成数クラス"] = item.name;
                changeBackgroundColor(item, this.icons.amount);
            }else if(this.initialSpec["呼び径"].includes(item.val) && item.name=="呼び径" ){
                this.specQuery["呼び径"] = item.val;
                this.nominal.model = item.val; 
            }else if(this.outer.isNecessary && this.initialSpec["外径か幅"].includes(item.val) && item.name=="外径か幅" ){
                this.specQuery["外径か幅"] = item.val;
                this.outer.model = this.specQuery["外径か幅"];
            }else if(this.thickness.isNecessary && this.initialSpec["長さか厚み"].includes(item.val) && item.name=="長さか厚み"){
                this.specQuery["長さか厚み"] = item.val;
                this.thickness.model = this.specQuery["長さか厚み"]; 
            }
            this.send_query();
        },
        resetQuery(){
            this.specQuery = {};
            this.send_query();
            for(let _key of Object.keys(this.carouselAndCard)){
                changeBackgroundColor({ name: "" }, this.icons[_key]);
            }
            this.nominal.model="";
            this.outer.model="";
            this.thickness.model="";
        },
        accessNextPage(){
            const _query = {}
            Object.assign(_query, this.shapeQuery,this.specQuery)
            this.$emit( 'emit-query', _query );
            this.$emit( 'emit-item-list', this.currentItems );
            if(this.itemQuantity == 1){
                this.$emit( 'emit-item', this.currentItems );
                this.$emit( 'emit-component-name', 'result' );
            }else{
                this.$emit( 'emit-component-name', 'result-list' );
            }
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        },
        backToPreviousPage(){
            this.resetQuery();
            this.$emit( 'emit-shape-query', {} );
            if(['めねじ','座金'].includes(this.genre)){
                this.$emit( 'emit-component-name', 'query-nut-washer-shape' );
            }else{
                this.$emit( 'emit-component-name', 'query-bolt-shape' );
            }
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        }
    }, 
    watch:{
        itemQuantity(){
            if (this.itemQuantity != 0){
                this.buttonDisabled = false;
            }else{
                this.buttonDisabled = true;
            }
        },
    },
    computed:{
        selectableMiddleClassification(){
            let _arr = [];
            this.icons.middle_classification.forEach((item) => {
                if(this.pickedMiddleClassification.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableMaterial(){
            let _arr = [];
            this.icons.material.forEach((item) => {
                if(this.pickedMaterial.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableSurface(){
            let _arr = [];
            this.icons.surface.forEach((item) => {
                if(this.pickedSurface.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableAmount(){
            let _arr = [];
            this.icons.amount.forEach((item) => {
                if(this.pickedAmount.includes(item.name)){
                    _arr.push(item);
                }
            });
            return _arr
        },
        selectableNominal(){
            let _arr = [];
            this.initialSpec["呼び径"].forEach((item) => {
                if(this.pickedNominal.includes(item)){
                    _arr.push({ "name":"呼び径", "val": item });
                }
            });
            return _arr
        },
        selectableOuter(){
            let _arr = [];
            this.initialSpec["外径か幅"].forEach((item) => {
                if(this.pickedOuter.includes(item)){
                    _arr.push({ "name":"外径か幅", "val": item });
                }
            });
            return _arr
        },
        selectableThickness(){
            let _arr = [];
            this.initialSpec["長さか厚み"].forEach((item) => {
                if(this.pickedThickness.includes(item)){
                    _arr.push({ "name":"長さか厚み", "val": item });
                }
            });
            return _arr
        },
    },
    created(){
        this.$vuetify.goTo(0);
        if(["おねじ","めねじ"].includes(this.genre)){
            this.outer.isNecessary = false;
            if(this.genre == "めねじ"){
                this.thickness.isNecessary = false;
                this.nominal.image = this.icons.nominal[1].src;
            }else{
                this.thickness.image = this.icons.thickness[0].src;
                this.nominal.image = this.icons.nominal[0].src;
            }
        }else{
            this.thickness.image = this.icons.thickness[1].src;
            this.nominal.image = this.icons.nominal[2].src;
            this.outer.image = this.icons.outer[0].src;
        }

        this.query = this.totalQuery;

        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {

                    if([1,3].includes(Object.keys(data.query).length)){
                        this.initialSpec = data.spec
                    }
                    if(!Object.keys(this.specQuery).includes("中分類")){
                        this.pickedMiddleClassification = data.spec["中分類"];
                    }

                    if(!Object.keys(this.specQuery).includes("材質")){
                        this.pickedMaterial = data.spec["材質"];
                    }
                    if(!Object.keys(this.specQuery).includes("表面処理")){
                        this.pickedSurface = data.spec["表面処理"];
                    }
                    if(!Object.keys(this.specQuery).includes("構成数クラス")){
                        this.pickedAmount = data.spec["構成数クラス"];
                    }
                    if(!Object.keys(this.specQuery).includes("呼び径")){
                        this.pickedNominal = data.spec["呼び径"];
                    }

                    if(["おねじ","座金"].includes(this.genre)){
                        if(!Object.keys(this.specQuery).includes("長さか厚み")){
                            this.pickedThickness = data.spec["長さか厚み"];
                        }
                    }
                    if(["座金"].includes(this.genre)){
                        if(!Object.keys(this.specQuery).includes("外径か幅")){
                            this.pickedOuter = data.spec["外径か幅"];
                        }
                    }
                    if(Object.keys(data).includes('items')){
                        this.currentItems = data.items;
                        this.itemQuantity = data.items.length;
                    }else{
                        this.currentItems = [];
                        this.itemQuantity = 0;
                    }
                    console.log(data);
                }
            )
            this.resetQuery();
        });
    },
    mounted(){
        this.$emit('add-step', 3);
    },
}
</script>
