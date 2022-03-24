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
                @click-back="removeSpecQuery"
                @click-next="fix_query"
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
                        v-model="selectedMiddleClassificationName"
                        :headerIsOn="true"
                        headerTitle="中分類"
                        :inputItems="selectableItems.middle_classification"
                        @update="send_query"
                        :labelIsOn="true"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        v-model="selectedMaterialName"
                        :headerIsOn="true"
                        headerTitle="材質"
                        :inputItems="selectableItems.material"
                        @update="send_query"
                        :labelIsOn="false"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        v-model="selectedSurfaceName"
                        :headerIsOn="true"
                        headerTitle="表面処理"
                        :inputItems="selectableItems.surface"
                        @update="send_query"
                        :labelIsOn="false"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        v-model="selectedAmountName"
                        :headerIsOn="true"
                        headerTitle="構成数クラス"
                        :inputItems="selectableItems.amount"
                        @update="send_query"
                        :labelIsOn="false"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <drop-down-menu
                        headerTitle="呼び径"
                        :imageSource="nominal.image"
                        v-model="nominal.model"
                        :inputItems="selectableItems.nominal"
                        @update="send_query"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4" v-if="outer.isNecessary">
                    <drop-down-menu
                        v-if="outer.isNecessary"
                        headerTitle="外径・幅"
                        :imageSource="outer.image"
                        v-model="outer.model"
                        :inputItems="selectableItems.outer"
                        @update="send_query"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <drop-down-menu
                        v-if="thickness.isNecessary"
                        headerTitle="長さ・厚さ"
                        :imageSource="thickness.image"
                        v-model="thickness.model"
                        :inputItems="selectableItems.thickness"
                        @update="send_query"
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
                @click-back="removeSpecQuery"
                @click-next="fix_query"
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
        syncStateReceiveRequestId: null,
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
        selectedMiddleClassificationName: null,
        selectedMaterialName: null,
        selectedSurfaceName: null,
        selectedAmountName: null,
    }),
    props:["duct","syncId","genre","shapeQuery"],
    methods: {
        send_query() {
            if (this.syncId === null) return;
            const _query = {}
            Object.assign(_query, this.shapeQuery,this.specQuery);
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId, 'genre': this.genre, 'query': _query},
            );
        },
        fix_query() {
            if (this.syncId === null) return;
            const _query = {}
            Object.assign(_query, this.shapeQuery, this.specQuery);
            this.$emit( 'emit-query', _query );
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId, 'genre': this.genre, 'query': _query, 'query_fixed': true },
            );
        },
        removeSpecQuery(){
            if (this.syncId === null) return;
            this.$emit( 'emit-shape-query', {} );
            let query = new Object(this.shapeQuery);
            switch(this.genre){
                case 'おねじ':
                    if (Object.keys(query).includes('頭部穴形状')){
                        delete query['頭部穴形状'];
                    } else if (Object.keys(query).includes('おねじ先端')){
                        delete query['おねじ先端'];
                    } else if (Object.keys(query).includes('頭部')){
                        delete query['頭部'];
                    }
                    break;
                case 'めねじ':
                    delete query['ナット形状'];
                    break;
                case '座金':
                    delete query['座金形状'];
                    break;
            }
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {
                    sync_id: this.syncId,
                    genre: this.genre,
                    query: query,
                },
            );
        },
        resetQuery(){
            const carouselAndCard = ['middle_classification', 'material', 'surface', 'amount'];
            this.send_query();
            for(let _key of carouselAndCard){
                changeBackgroundColor({ name: "" }, this.icons[_key]);
            }
        },
        accessNextPage(){
            const _query = {}
            Object.assign(_query, this.shapeQuery,this.specQuery)
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
            if(['めねじ','座金'].includes(this.genre)){
                this.$emit( 'emit-component-name', 'query-nut-washer-shape' );
            }else{
                this.$emit( 'emit-component-name', 'query-bolt-shape' );
            }
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        },
        registerSyncStateReceiveHandler(){
            this.$emit(
                'register-sync-state-receive-handler',
                {
                    rid: this.syncStateReceiveRequestId,
                    handler: (rid, eid, data) => {
                        if(!Object.keys(data).includes('spec')){
                            this.backToPreviousPage();
                        }else{
                            if (Object.keys(data).includes('query_fixed')) {
                                this.accessNextPage();
                            } else {
                                if([1,3].includes(Object.keys(data.query).length)) this.initialSpec = data.spec;

                                let dataQueryKeys = Object.keys(data.query);
                                if(dataQueryKeys.includes('中分類')){
                                    this.selectedMiddleClassificationName = data.query['中分類'];
                                }else{
                                    this.selectedMiddleClassificationName = null;
                                }
                                if(dataQueryKeys.includes('材質')){
                                    this.selectedMaterialName = data.query['材質'];
                                }else{
                                    this.selectedMaterialName = null;
                                }
                                if(dataQueryKeys.includes('表面処理')){
                                    this.selectedSurfaceName = data.query['表面処理'];
                                }else{
                                    this.selectedSurfaceName = null;
                                }
                                if(dataQueryKeys.includes('構成数クラス')){
                                    this.selectedAmountName = data.query['構成数クラス'];
                                }else{
                                    this.selectedAmountName = null;
                                }
                                if(dataQueryKeys.includes('呼び径')){
                                    this.nominal.model = data.query['呼び径'];
                                }else{
                                    this.nominal.model = null;
                                }
                                if(dataQueryKeys.includes('外径か幅')){
                                    this.outer.model = data.query['外径か幅'];
                                }else{
                                    this.outer.model = null;
                                }
                                if(dataQueryKeys.includes('長さか厚み')){
                                    this.thickness.model = data.query['長さか厚み'];
                                }else{
                                    this.thickness.model = null;
                                }

                                for(let _key in this.selectableItemValues){
                                    if(!["長さか厚み","外径か幅"].includes(_key)){
                                        this.selectableItemValues[_key] = data.spec[_key];
                                    }else if(_key == "長さか厚み"){
                                        if(["おねじ","座金"].includes(this.genre)) this.selectableItemValues[_key] = data.spec[_key];
                                    }else{
                                        if(["座金"].includes(this.genre)) this.selectableItemValues[_key] = data.spec[_key];
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
                        }
                    },
                },
            );
        },
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
        specQuery(){
            let specQuery = {};
            if (this.selectedMiddleClassificationName !== null) {
                specQuery['中分類'] = this.selectedMiddleClassificationName;
            }
            if (this.selectedMaterialName !== null) {
                specQuery['材質'] = this.selectedMaterialName;
            }
            if (this.selectedSurfaceName !== null) {
                specQuery['表面処理'] = this.selectedSurfaceName;
            }
            if (this.selectedAmountName !== null) {
                specQuery['構成数クラス'] = this.selectedAmountName;
            }
            if (this.nominal.model !== null) {
                specQuery['呼び径'] = this.nominal.model;
            }
            if (this.outer.model !== null) {
                specQuery['外径か幅'] = this.outer.model;
            }
            if (this.thickness.model !== null) {
                specQuery['長さか厚み'] = this.thickness.model;
            }
            return specQuery;
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
        this.syncStateReceiveRequestId = this.duct.nextRid();
        this.$emit(
            'register-sync-state-receive-handler',
            {
                rid: this.syncStateReceiveRequestId,
                handler: async (rid, eid, data) => {
                    let initialSyncState = data;
                    data = await this.duct.call(
                        this.duct.EVENT.NEJI,
                        {
                            genre: this.genre,
                            query: this.shapeQuery,
                        },
                    );

                    for(let _key in this.selectableItemValues){
                        if(!["長さか厚み","外径か幅"].includes(_key)){
                            this.selectableItemValues[_key] = data.spec[_key];
                        }else if(_key == "長さか厚み"){
                            if(["おねじ","座金"].includes(this.genre)) this.selectableItemValues[_key] = data.spec[_key];
                        }else{
                            if(["座金"].includes(this.genre)) this.selectableItemValues[_key] = data.spec[_key];
                        }
                    }

                    let initialQueryKeys = Object.keys(initialSyncState.query);
                    if(initialQueryKeys.includes('中分類')){
                        this.selectedMiddleClassificationName = initialSyncState.query['中分類'];
                    }
                    if(initialQueryKeys.includes('材質')){
                        this.selectedMaterialName = initialSyncState.query['材質'];
                    }
                    if(initialQueryKeys.includes('表面処理')){
                        this.selectedSurfaceName = initialSyncState.query['表面処理'];
                    }
                    if(initialQueryKeys.includes('構成数クラス')){
                        this.selectedAmountName = initialSyncState.query['構成数クラス'];
                    }
                    if(initialQueryKeys.includes('呼び径')){
                        this.nominal.model = initialSyncState.query['呼び径'];
                    }
                    if(initialQueryKeys.includes('外径か幅')){
                        this.outer.model = initialSyncState.query['外径か幅'];
                    }
                    if(initialQueryKeys.includes('長さか厚み')){
                        this.thickness.model = initialSyncState.query['長さか厚み'];
                    }
                    let query = {}
                    Object.assign(query, this.shapeQuery, this.specQuery);
                    data = await this.duct.call(
                        this.duct.EVENT.NEJI,
                        {
                            genre: this.genre,
                            query: query,
                        },
                    );

                    if(Object.keys(data).includes('items')){
                        this.currentItems = data.items;
                        this.itemQuantity = data.items.length;
                    }else{
                        this.currentItems = [];
                        this.itemQuantity = 0;
                    }

                    this.registerSyncStateReceiveHandler();
                },
            },
        );
    },
    mounted(){
        this.$emit('add-step', 3);
    },
    destroyed(){
        this.$emit(
            'unregister-sync-state-receive-handler',
            { rid: this.syncStateReceiveRequestId },
        );
    },
}
</script>
