<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>おねじの形状を選ぶ</v-card-title>
        <v-card-text> 
            <v-row>
                <v-col cols="12" md="4">
                    <card-button 
                        v-model="selectedHeadName"
                        header-title="頭部の形状を選ぶ"
                        :input-items="selectableHeadIcons"
                        :label-is-on="true"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <v-slide-y-transition>
                        <carousel-button
                           v-if="isPicked.head"
                           header-title="おねじ先端の形状を選ぶ"
                           v-model="selectedTipName"
                           :input-items="selectableTipIcons"
                           class="mb-6"
                        />
                    </v-slide-y-transition>
                </v-col>
                <v-col cols="12" md="4">
                    <v-slide-y-transition>
                        <carousel-button
                            v-if="isPicked.tip"
                            v-model="selectedHoleShapeName"
                            header-title="頭部穴の形状を選ぶ"
                            :input-items="selectableHoleShapeIcons"
                            class="mb-6"
                        />
                    </v-slide-y-transition>
                </v-col>
            </v-row>
            <v-divider class="pt-3"/>
            <page-transition-button 
                :click-back-callback="unsetGenre"
            />
        </v-card-text>   
    </v-card>
</template>
<script>
import { Duct } from '@iflb/ducts-client'
import CardButton from '../../CardButton'
import CarouselButton from '../../CarouselButton'
import PageTransitionButton from '../../PageTransitionButton'
import { bolt_icons } from '../../shape_profile.js'

const shapeKey = {
    head: '頭部', 
    tip: 'おねじ先端', 
    hole_shape: '頭部穴形状'
};
export default{
    watch: {
        selectedHeadName() {
            this.selectedTipName = null;
            this.send_query();
        },
        selectedTipName() {
            this.selectedHoleShapeName = null;
            this.send_query();
        },
        selectedHoleShapeName() {
            this.send_query();
        },
    },

    components:{
        CardButton,
        CarouselButton,
        PageTransitionButton
    },
    data: () => ({
        selectableTipNames:[],
        selectableHoleShapeNames:[],
        syncStateReceiveRequestId: null,
        selectedHeadName: null,
        selectedTipName: null,
        selectedHoleShapeName: null,
    }),

    props: {
        duct: { type: Duct },
        syncId: { type: String },
        genre: { type: String },
        shapeQuery: { type: Object },
    },

    computed:{
        isPicked() {
            return {
                head: (this.selectedHeadName !== null),
                tip: (this.selectedTipName !== null),
                hole_shape: (this.selectedHoleShapeName !== null),
            };
        },
        selectableHeadIcons() {
            return bolt_icons.head;
        },
        selectableTipIcons(){
            return bolt_icons.tip.filter(item => this.selectableTipNames.includes(item.name));
        },
        selectableHoleShapeIcons(){
            return bolt_icons.hole_shape.filter(item => this.selectableHoleShapeNames.includes(item.name));
        },
        query(){
            let query = {};
            if (this.selectedHeadName !== null) {
                query[shapeKey.head] = this.selectedHeadName;
            }
            if (this.selectedTipName !== null) {
                query[shapeKey.tip] = this.selectedTipName;
            }
            if (this.selectedHoleShapeName !== null) {
                query[shapeKey.hole_shape] = this.selectedHoleShapeName;
            }
            return query;
        },
    },
    methods: {
        send_query() {
            if (this.syncId === null) return;
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {'sync_id': this.syncId,'genre': this.genre, 'query': this.query},
            );
        },
        unsetGenre(){
            if (this.syncId === null) return;
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {
                    sync_id: this.syncId,
                },
            );
        },
        accessNextPage(){
            this.$emit( 'emit-query', this.query );
            this.$emit( 'emit-component-name', 'query-spec' );
        },
        backToPreviousPage(){
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
                            if(Object.keys(data.query).includes("頭部")){
                                this.selectedHeadName = data.query["頭部"];
                            }
                            if(!Object.keys(data.query).includes("おねじ先端")){
                                this.selectableTipNames = data.shape["おねじ先端"];
                            } else {
                                this.selectedTipName = data.query["おねじ先端"];
                            }
                            if(!Object.keys(data.query).includes("頭部穴形状")){
                                this.selectableHoleShapeNames = data.shape["頭部穴形状"]
                            } else {
                                this.selectedHoleShapeName = data.query["頭部穴形状"];
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
                    let shapeKeyHead = shapeKey.head;
                    if(!Object.keys(initialSyncState.query).includes(shapeKeyHead)){
                        this.registerSyncStateReceiveHandler();
                        return;
                    }
                    this.selectedHeadName = initialSyncState.query[shapeKeyHead];
                    data = await this.duct.call(
                        this.duct.EVENT.NEJI,
                        {
                            genre: this.genre,
                            query: this.query,
                        },
                    );
                    this.selectableTipNames = data.shape[shapeKey.tip];
                    if(!Object.keys(initialSyncState.query).includes(shapeKey.tip)){
                        this.registerSyncStateReceiveHandler();
                        return;
                    }
                    this.selectedTipName = initialSyncState.query[shapeKey.tip];
                    data = await this.duct.call(
                        this.duct.EVENT.NEJI,
                        {
                            genre: this.genre,
                            query: this.query,
                        },
                    );
                    this.selectableHoleShapeNames = data.shape[shapeKey.hole_shape];
                    if(Object.keys(initialSyncState.query).includes(shapeKey.hole_shape)){
                        this.registerSyncStateReceiveHandler();
                        return;
                    }
                    this.selectedHoleShapeName = initialSyncState.query[shapeKey.hole_shape];
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

