<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
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
                        :inputItems="selectableItems.middle_classification"
                        @update-query="makeQuery"
                        :labelIsOn="true"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        :headerIsOn="true"
                        headerTitle="材質"
                        :inputItems="selectableItems.material"
                        @update-query="makeQuery"
                        :labelIsOn="false"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        :headerIsOn="true"
                        headerTitle="表面処理"
                        :inputItems="selectableItems.surface"
                        @update-query="makeQuery"
                        :labelIsOn="false"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        :headerIsOn="true"
                        headerTitle="構成数クラス"
                        :inputItems="selectableItems.amount"
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
                        :inputItems="selectableItems.nominal"
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
                        :inputItems="selectableItems.outer"
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
                        :inputItems="selectableItems.thickness"
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
        specQuery:{}, 
        snackbar:false,
        initialSpec:{
            "中分類": [],
            "材質": [],
            "表面処理": [],
            "構成数クラス": [],
            "呼び径": [],
            "外径か幅": [],
            "長さか厚み": [],
        },
        selectableItemValues:{
            "中分類": [],
            "材質": [],
            "表面処理": [],
            "構成数クラス": [],
            "呼び径": [],
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
        itemQuantity:0,
        buttonDisabled:true,
        currentItems:[],
    }),
    props:["duct","syncId","genre","shapeQuery"],
    methods: {
        send_query() {
            if (this.syncId === null) return;
            const _query = {}
            Object.assign(_query, this.shapeQuery,this.specQuery);
            console.log(_query);
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId, 'genre': this.genre, 'query': _query},
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
            const carouselAndCard = ['middle_classification', 'material', 'surface', 'amount'];
            this.specQuery = {};
            this.send_query();
            for(let _key of carouselAndCard){
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
        selectableItems(){
            let _obj = {
                "middle_classification": [],
                "material": [],
                "surface": [],
                "amount": [],
                "nominal": [],
                "outer": [],
                "thickness": [],
            };
            const _language = {
                "中分類": 'middle_classification',
                "材質": 'material',
                "表面処理": 'surface',
                "構成数クラス": 'amount',
                "呼び径": 'nominal',
                "外径か幅": 'outer',
                "長さか厚み": 'thickness',
            };

            for(let _key in _language){
                const _eng = _language[_key];
                if(["中分類","材質","表面処理","構成数クラス"].includes(_key)){
                    this.icons[_eng].forEach((item) => {
                        if(this.selectableItemValues[_key].includes(item.name)) _obj[_eng].push(item);
                    });
                }else{
                    if(typeof this.initialSpec[_key] != 'undefined'){
                        this.initialSpec[_key].forEach((item) => {
                            if(this.selectableItemValues[_key].includes(item)) _obj[_eng].push({ "name": _key, "val": item });
                        });
                    }
                }
            }
            return _obj
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
        this.$emit(
            'register-page-specific-sync-manager-response-handler',
            {
                id: 'query-spec',
                handler: (rid, eid, data) => {
                    if (data.entry_type === 'StateEntry') {
                        if([1,3].includes(Object.keys(data.query).length)) this.initialSpec = data.spec;

                        for(let _key in this.selectableItemValues){
                            if(!Object.keys(this.specQuery).includes(_key)){
                                if(!["長さか厚み","外径か幅"].includes(_key)){
                                    this.selectableItemValues[_key] = data.spec[_key];
                                }else if(_key == "長さか厚み"){
                                    if(["おねじ","座金"].includes(this.genre)) this.selectableItemValues[_key] = data.spec[_key];
                                }else{
                                    if(["座金"].includes(this.genre)) this.selectableItemValues[_key] = data.spec[_key];
                                }
                            }
                        }

                        if(Object.keys(data).includes('items')){
                            this.currentItems = data.items;
                            this.itemQuantity = data.items.length;
                        }else{
                            this.currentItems = [];
                            this.itemQuantity = 0;
                        }
                    }
                },
            },
        );
        this.duct.invokeOnOpen(this.resetQuery);
    },
    mounted(){
        this.$emit('add-step', 3);
    },
    destroyed(){
        this.$emit(
            'unregister-page-specific-sync-manager-response-handler',
            { id: 'query-spec' },
        );
    },
}
</script>
