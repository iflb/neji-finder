<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>おねじの形状を選ぶ</v-card-title>
        <v-card-text> 
            <v-row>
                <v-col cols="12" md="4">
                    <card-button 
                        :headerIsOn="true"
                        headerTitle="頭部の形状"
                        :inputItems="bolt_icons.head"
                        @update-query="makeQuery"
                        :labelIsOn="true"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <v-slide-y-transition>
                        <carousel-button
                           v-if="isPicked.head"
                           :headerIsOn="true"
                           headerTitle="おねじ先端の形状"
                           :inputItems="selectableTip"
                           @update-query="makeQuery"
                           class="mb-6"
                        />
                    </v-slide-y-transition>
                </v-col>
                <v-col cols="12" md="4">
                    <v-slide-y-transition>
                        <carousel-button
                            v-if="isPicked.tip"
                            :headerIsOn="true"
                            headerTitle="頭部穴の形状"
                            :inputItems="selectableHoleShape"
                            @update-query="makeQuery"
                            class="mb-6"
                        />
                    </v-slide-y-transition>
                </v-col>
            </v-row>
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
        isPicked: { head:false, tip:false, hole_shape:false },
        pickedTip:[],
        pickedHoleShape:[],
        query: {},
        shape: {},
        shapeKey: {
            'head': '頭部', 
            'tip': 'おねじ先端', 
            'hole_shape': '頭部穴形状'
        },
        nextPage:true,
    }),
    props:["duct","syncId","genre","shapeQuery"],
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
        makeQuery(item){
            this.nextPage = true;
            for(let _key in this.shapeKey){
                const _shapeType = this.bolt_icons[_key];
                if(_shapeType.includes(item)){
                    if(_key === 'head'){
                        this.query = {};
                        for (let _key in this.isPicked){
                            this.isPicked[_key] = false;
                        }
                        for (let _key in this.shapeKey){
                            changeBackgroundColor({ name: '' }, this.bolt_icons[_key]);
                        }
                        changeBackgroundColor( item, this.bolt_icons[_key] );
                    }else{
                        changeBackgroundColor( item, this.bolt_icons[_key]);
                    }
                    this.isPicked[_key] = true;
                    this.query[this.shapeKey[_key]] = item.name;
                    this.send_query();
                }
            }
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
            this.query = {};
            this.$emit( 'emit-query', this.query );
            this.$emit( 'emit-component-name', 'query-genre' );
        }
    }, 
    created(){
        this.nextPage = false;
        this.$emit(
            'register-page-specific-sync-manager-response-handler',
            {
                id: 'query-bolt-shape',
                handler: (rid, eid, data) => {
                    if (data.entry_type === 'StateEntry') {
                        this.$set(this, 'query', 'query' in data && Object.keys(data.query).length > 0 ? data.query : {});
                        this.$set(this, 'shape', 'shape' in data ? data.shape : '');

                        if(!Object.keys(this.query).includes("おねじ先端")){
                            this.pickedTip = this.shape["おねじ先端"];
                        }
                        if(!Object.keys(this.query).includes("頭部穴形状")){
                            this.pickedHoleShape = this.shape["頭部穴形状"];
                        }

                        if(Object.keys(this.query).length === 3 && this.nextPage){
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
        this.duct.invokeOnOpen(this.send_query);
    },
    mounted(){
        this.$emit('add-step', 2);
    },
    destroyed(){
        this.$emit(
            'unregister-page-specific-sync-manager-response-handler',
            { id: 'query-bolt-shape' },
        );
    },
}
</script>

