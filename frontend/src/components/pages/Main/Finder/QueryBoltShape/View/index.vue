<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>おねじの形状を選ぶ</v-card-title>
        <v-card-text> 
            <v-row>
                <v-col cols="12" md="4">
                    <card-button 
                        v-model="selectedHeadName"
                        :headerIsOn="true"
                        headerTitle="頭部の形状"
                        :inputItems="selectableHead"
                        @update-query="getTips"
                        :labelIsOn="true"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <v-slide-y-transition>
                        <carousel-button
                           v-if="isPicked.head"
                           v-model="selectedTipName"
                           :headerIsOn="true"
                           headerTitle="おねじ先端の形状"
                           :inputItems="selectableTip"
                           @update-query="getHoleShapes"
                           class="mb-6"
                        />
                    </v-slide-y-transition>
                </v-col>
                <v-col cols="12" md="4">
                    <v-slide-y-transition>
                        <carousel-button
                            v-if="isPicked.tip"
                            v-model="selectedHoleShapeName"
                            :headerIsOn="true"
                            headerTitle="頭部穴の形状"
                            :inputItems="selectableHoleShape"
                            @update-query="getSpecs"
                            class="mb-6"
                        />
                    </v-slide-y-transition>
                </v-col>
            </v-row>
            <v-divider class="pt-3"/>
            <page-transition-button 
                :nextIsNecessary="false"
                @click-back="unsetGenre"
            />
        </v-card-text>   
    </v-card>
</template>
<script>
import CardButton from '../../CardButton'
import CarouselButton from '../../CarouselButton'
import PageTransitionButton from '../../PageTransitionButton'
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
        CarouselButton,
        PageTransitionButton
    },
    data: () => ({
        bolt_icons,
        pickedTip:[],
        pickedHoleShape:[],
        query: {},
        shape: {},
        shapeKey: {
            'head': '頭部', 
            'tip': 'おねじ先端', 
            'hole_shape': '頭部穴形状'
        },
        syncStateReceiveRequestId: null,
        selectedHeadName: null,
        selectedTipName: null,
        selectedHoleShapeName: null,
    }),
    props:["duct","syncId","genre","shapeQuery"],
    computed:{
        isPicked() {
            return {
                head: (this.selectedHeadName !== null),
                tip: (this.selectedTipName !== null),
                hole_shape: (this.selectedHoleShapeName !== null),
            };
        },
        selectableHead() {
            return this.bolt_icons.head;
        },
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
            if (this.syncId === null) return;
            let _query = {};
            if (this.query){
                _query = this.query;
            }
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId,'genre': this.genre, 'query': _query},
            );
        },
        unsetGenre(){
            this.query = {};
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {
                    sync_id: this.syncId,
                    query: this.query,
                },
            );
        },
        getTips(item){
            this.query[this.shapeKey.head] = item.name;
            this.send_query();
        },
        getHoleShapes(item){
            this.query[this.shapeKey.tip] = item.name;
            this.send_query();
        },
        getSpecs(item){
            this.query[this.shapeKey.hole_shape] = item.name;
            this.send_query();
        },
        accessNextPage(){
            for (let _key in this.shapeKey){
                changeBackgroundColor({ name: '' }, this.bolt_icons[_key]);
            }
            this.$emit( 'emit-query', this.query );
            this.$emit( 'emit-component-name', 'query-spec' );
        },
        backToPreviousPage(){
            for (let _key in this.shapeKey){
                changeBackgroundColor({ name: '' }, this.bolt_icons[_key]);
            }
            this.$emit( 'emit-query', this.query );
            this.$emit( 'emit-component-name', 'query-genre' );
        },
        registerSyncStateReceiveHandler(){
            this.$emit(
                'register-sync-state-receive-handler',
                {
                    rid: this.syncStateReceiveRequestId,
                    handler: (rid, eid, data) => {
                        if(!Object.keys(data).includes('genre')){
                            this.backToPreviousPage();
                        }else{
                            this.$set(this, 'query', 'query' in data && Object.keys(data.query).length > 0 ? data.query : {});
                            this.$set(this, 'shape', 'shape' in data ? data.shape : '');

                            if(Object.keys(this.query).includes("頭部")){
                                this.selectedHeadName = this.query["頭部"];
                            }
                            if(!Object.keys(this.query).includes("おねじ先端")){
                                this.pickedTip = this.shape["おねじ先端"];
                            } else {
                                this.selectedTipName = this.query["おねじ先端"];
                            }
                            if(!Object.keys(this.query).includes("頭部穴形状")){
                                this.pickedHoleShape = this.shape["頭部穴形状"]
                            } else {
                                this.selectedHoleShape = this.query["頭部穴形状"];
                            }

                            if(Object.keys(data).includes('spec')){
                                this.accessNextPage();
                            }else{
                                if(!['md','lg','xl'].includes(this.$vuetify.breakpoint.name)){
                                    this.$nextTick(() => {
                                        this.$vuetify.goTo(document.body.scrollHeight);
                                    });
                                }
                            }
                        }
                    },
                },
            );
        },
    }, 
    created(){
        this.syncStateReceiveRequestId = this.duct.nextRid();
        this.$emit(
            'register-sync-state-receive-handler',
            {
                rid: this.syncStateReceiveRequestId,
                handler: async (rid, eid, data) => {
                    let initialSyncState = data;
                    this.query = {};
                    let shapeKeyHead = this.shapeKey.head;
                    if(!Object.keys(initialSyncState.query).includes(shapeKeyHead)){
                        this.registerSyncStateReceiveHandler();
                        return;
                    }
                    let selectedHeadName = initialSyncState.query[shapeKeyHead];
                    this.query[shapeKeyHead] = selectedHeadName;
                    this.selectedHeadName = this.selectableHead
                        .map(selectableHead => selectableHead.name)
                        .find(selectableHeadName => (selectedHeadName === selectableHeadName));
                    data = await this.duct.call(
                        this.duct.EVENT.NEJI,
                        {
                            genre: this.genre,
                            query: this.query,
                        },
                    );
                    let shapeKeyTip = this.shapeKey.tip;
                    let selectableTipNames = data.shape[shapeKeyTip];
                    this.pickedTip = selectableTipNames;
                    if(!Object.keys(initialSyncState.query).includes(shapeKeyTip)){
                        this.registerSyncStateReceiveHandler();
                        return;
                    }
                    let selectedTipName = initialSyncState.query[shapeKeyTip];
                    this.query[shapeKeyTip] = selectedTipName;
                    this.selectedTipName = this.selectableTip
                        .map(selectableTip => selectableTip.name)
                        .find(selectableTipName => (selectedTipName === selectableTipName));
                    data = await this.duct.call(
                        this.duct.EVENT.NEJI,
                        {
                            genre: this.genre,
                            query: this.query,
                        },
                    );
                    let shapeKeyHoleShape = this.shapeKey.hole_shape;
                    let selectableHoleShapeNames = data.shape[shapeKeyHoleShape];
                    this.pickedHoleShape = selectableHoleShapeNames;
                    if(Object.keys(initialSyncState.query).includes(shapeKeyHoleShape)){
                        this.registerSyncStateReceiveHandler();
                        return;
                    }
                    let selectedHoleShapeName = initialSyncState.query[shapeKeyHoleShape];
                    this.query[shapeKeyHoleShape] = selectedHoleShapeName;
                    this.selectedHoleShapeName = this.selectableHoleShape
                        .map(selectableHoleShape => selectableHoleShape.name)
                        .find(selectableHoleShapeName => (selectedHoleShapeName === selectableHoleShapeName));
                    this.registerSyncStateReceiveHandler();
                },
            },
        );
    },
    mounted(){
        this.$emit('add-step', 2);
    },
    destroyed(){
        this.$emit(
            'unregister-sync-state-receive-handler',
            { rid: this.syncStateReceiveRequestId },
        );
    },
}
</script>

