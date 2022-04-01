<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の規格を選ぶ</v-card-title>
        <v-card-text> 
            <v-row>
                <v-col>
                    <span class="text-body-1">{{ itemQuantityMessage }}</span>
                </v-col>
            </v-row>
            <page-transition-button 
                :next-disabled="isItemQuantityTooMany"
                :click-back-callback="removeSpecQuery"
                :click-next-callback="fix_query"
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
                        header-title="中分類を選ぶ"
                        :input-items="selectableMiddleClassificationIcons"
                        shows-label
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        v-model="selectedMaterialName"
                        header-title="材質を選ぶ"
                        :input-items="selectableMaterialIcons"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        v-model="selectedSurfaceName"
                        header-title="表面処理を選ぶ"
                        :input-items="selectableSurfaceIcons"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <card-button 
                        v-model="selectedAmountName"
                        header-title="構成数クラス"
                        :input-items="selectableAmountIcons"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4">
                    <drop-down-menu
                        header-title="呼び径を選ぶ"
                        :imageSource="nominalImage"
                        v-model="selectedNominal"
                        :input-items="selectableNominalValues"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4" v-if="outerImage !== null">
                    <drop-down-menu
                        header-title="外径・幅を選ぶ"
                        :imageSource="outerImage"
                        v-model="selectedOuter"
                        :input-items="selectableOuterValues"
                        class="mb-6"
                    />
                </v-col>
                <v-col cols="12" md="4" v-if="thicknessImage !== null">
                    <drop-down-menu
                        header-title="長さ・厚さを選ぶ"
                        :imageSource="thicknessImage"
                        v-model="selectedThickness"
                        :input-items="selectableThicknessValues"
                        class="mb-6"
                    />
                </v-col>
            </v-row>
            <v-divider />
            <v-row class="pt-3">
                <v-col>
                    <span class="text-body-1">{{ itemQuantityMessage }}</span>
                </v-col>
            </v-row>
            <page-transition-button 
                :next-disabled="isItemQuantityTooMany"
                :click-back-callback="removeSpecQuery"
                :click-next-callback="fix_query"
            />
        </v-card-text>   
    </v-card>
</template>
<script>
import { Duct } from '@iflb/ducts-client'
import { icons } from '../../spec_profile.js'
import CardButton from '../../CardButton'
import CarouselButton from '../../CarouselButton'
import DropDownMenu from '../../DropDownMenu'
import PageTransitionButton from '../../PageTransitionButton'

const specKeyToIconKey = {
    '中分類': 'middle_classification',
    '材質': 'material',
    '表面処理': 'surface',
    '構成数クラス': 'amount',
    '呼び径': 'nominal',
    '外径か幅': 'outer',
    '長さか厚み': 'thickness',
};

const specKeys = Object.keys(specKeyToIconKey);

export default{
    components: {
        CardButton,
        DropDownMenu,
        CarouselButton,
        PageTransitionButton
    },
    data() {
        let initialSpec = {};
        let selectableItemValues = {};
        for (let specKey of specKeys) {
            initialSpec[specKey] = [];
            selectableItemValues[specKey] = [];
        }
        return {
            syncStateReceiveRequestId: null,
            initialSpec: initialSpec,
            selectableItemValues: selectableItemValues,
            currentItems: null,
            selectedMiddleClassificationName: null,
            selectedMaterialName: null,
            selectedSurfaceName: null,
            selectedAmountName: null,
            selectedNominal: null,
            selectedOuter: null,
            selectedThickness: null,
        };
    },

    props: {
        duct: { type: Duct },
        syncId: { type: String },
        genre: { type: String },
        shapeQuery: { type: Object },
    },

    methods: {
        send_query() {
            if (this.syncId === null) return;
            let query = {}
            Object.assign(query, this.shapeQuery, this.specQuery);
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

        fix_query() {
            if (this.syncId === null) return;
            const query = {}
            Object.assign(query, this.shapeQuery, this.specQuery);
            this.$emit('emit-query', query);
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.SYNC_STATE_UPDATE,
                {
                    sync_id: this.syncId,
                    genre: this.genre,
                    query: query,
                    query_fixed: true,
                },
            );
        },

        removeSpecQuery() {
            if (this.syncId === null) return;
            this.$emit('emit-shape-query', {});
            let query = new Object(this.shapeQuery);
            switch (this.genre) {
                case 'おねじ':
                    if (Object.keys(query).includes('頭部穴形状')) {
                        delete query['頭部穴形状'];
                    } else if (Object.keys(query).includes('おねじ先端')) {
                        delete query['おねじ先端'];
                    } else if (Object.keys(query).includes('頭部')) {
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

        resetQuery() {
            this.selectedMiddleClassificationName = null;
            this.selectedMaterialName = null;
            this.selectedSurfaceName = null;
            this.selectedAmountName = null;
            this.selectedNominal = null;
            this.selectedOuter = null;
            this.selectedThickness = null;
            this.send_query();
        },

        accessNextPage() {
            console.assert(this.currentItem !== null);
            this.$emit('emit-item-list', this.currentItems);
            if (this.itemQuantity === 1) {
                this.$emit('emit-item', this.currentItems[0]);
                this.$emit('emit-component-name', 'result');
            } else {
                this.$emit('emit-component-name', 'result-list');
            }
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        },

        backToPreviousPage() {
            if (['めねじ','座金'].includes(this.genre)) {
                this.$emit('emit-component-name', 'query-nut-washer-shape');
            } else {
                this.$emit('emit-component-name', 'query-bolt-shape');
            }
            this.$nextTick(() => {
                this.$vuetify.goTo(0);
            });
        },

        registerSyncStateReceiveHandler() {
            this.$emit(
                'register-sync-state-receive-handler',
                {
                    rid: this.syncStateReceiveRequestId,
                    handler: (rid, eid, data) => {
                        if (!Object.keys(data).includes('spec')) {
                            this.backToPreviousPage();
                        } else {
                            if (Object.keys(data).includes('query_fixed')) {
                                this.accessNextPage();
                            } else {
                                let dataQueryKeys = Object.keys(data.query);
                                if (dataQueryKeys.includes('中分類')) {
                                    this.selectedMiddleClassificationName = data.query['中分類'];
                                } else {
                                    this.selectedMiddleClassificationName = null;
                                }
                                if (dataQueryKeys.includes('材質')) {
                                    this.selectedMaterialName = data.query['材質'];
                                } else {
                                    this.selectedMaterialName = null;
                                }
                                if (dataQueryKeys.includes('表面処理')) {
                                    this.selectedSurfaceName = data.query['表面処理'];
                                } else {
                                    this.selectedSurfaceName = null;
                                }
                                if (dataQueryKeys.includes('構成数クラス')) {
                                    this.selectedAmountName = data.query['構成数クラス'];
                                } else {
                                    this.selectedAmountName = null;
                                }
                                if (dataQueryKeys.includes('呼び径')) {
                                    this.selectedNominal = data.query['呼び径'];
                                } else {
                                    this.selectedNominal = null;
                                }
                                if (dataQueryKeys.includes('外径か幅')) {
                                    this.selectedOuter = data.query['外径か幅'];
                                } else {
                                    this.selectedOuter = null;
                                }
                                if (dataQueryKeys.includes('長さか厚み')) {
                                    this.selectedThickness = data.query['長さか厚み'];
                                } else {
                                    this.selectedThickness = null;
                                }

                                for (let [ specKey, specValue ] of Object.entries(data.spec)) {
                                    this.selectableItemValues[specKey] = specValue;
                                }

                                if (Object.keys(data).includes('items')) {
                                    this.currentItems = data.items;
                                } else {
                                    this.currentItems = null;
                                }
                            }
                        }
                    },
                },
            );
        },
    }, 

    watch: {
        selectedMiddleClassificationName() { this.send_query() },
        selectedMaterialName() { this.send_query() },
        selectedSurfaceName() { this.send_query() },
        selectedAmountName() { this.send_query() },
        selectedNominal() { this.send_query() },
        selectedOuter() { this.send_query() },
        selectedThickness() { this.send_query() },
    },

    computed: {
        selectableIcons() {
            let selectableIcons = {};
            for (let specKey of [ '中分類', '材質', '表面処理', '構成数クラス' ]) {
                let iconKey = specKeyToIconKey[specKey];
                selectableIcons[specKey] = icons[iconKey].filter(icon => this.selectableItemValues[specKey].includes(icon.name));
            }
            return selectableIcons;
        },
        selectableMiddleClassificationIcons() { return this.selectableIcons['中分類'] },
        selectableMaterialIcons() { return this.selectableIcons['材質'] },
        selectableSurfaceIcons() { return this.selectableIcons['表面処理'] },
        selectableAmountIcons() { return this.selectableIcons['構成数クラス'] },

        selectableValues() {
            let selectableValues = {};
            for (let specKey of [ '呼び径', '外径か幅', '長さか厚み' ]) {
                if (Object.keys(this.initialSpec).includes(specKey)) {
                    selectableValues[specKey] = this.initialSpec[specKey]
                        .filter(value => this.selectableItemValues[specKey].includes(value))
                        .map(value => ({ name: specKey, val: value }));
                } else {
                    selectableValues[specKey] = [];
                }
            }
            return selectableValues;
        },
        selectableNominalValues() { return this.selectableValues['呼び径'] },
        selectableOuterValues() { return this.selectableValues['外径か幅'] },
        selectableThicknessValues() { return this.selectableValues['長さか厚み'] },

        specQuery() {
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
            if (this.selectedNominal !== null) {
                specQuery['呼び径'] = this.selectedNominal;
            }
            if (this.selectedOuter !== null) {
                specQuery['外径か幅'] = this.selectedOuter;
            }
            if (this.selectedThickness !== null) {
                specQuery['長さか厚み'] = this.selectedThickness;
            }
            return specQuery;
        },

        nominalImage() {
            switch (this.genre) {
                case 'おねじ':
                    return icons.nominal[0].src;
                case 'めねじ':
                    return icons.nominal[1].src;
                case '座金':
                    return icons.nominal[2].src;
                default:
                    return null;
            }
        },

        thicknessImage() {
            switch (this.genre) {
                case 'おねじ':
                    return icons.thickness[0].src;
                case '座金':
                    return icons.thickness[1].src;
                default:
                    return null;
            }
        },

        outerImage() {
            switch (this.genre) {
                case '座金':
                    return icons.outer[0].src;
                default:
                    return null;
            }
        },

        itemQuantity() {
            if (this.currentItems === null) return null;
            return this.currentItems.length;
        },

        isItemQuantityTooMany() {
            return (this.itemQuantity === null);
        },

        itemQuantityMessage() {
            if (this.isItemQuantityTooMany) {
                return '該当件数が多すぎます。絞り込んでください';
            } else {
                return '該当商品数：' + String(this.itemQuantity) + '個';
            }
        },
    },

    created() {
        this.$vuetify.goTo(0);
        this.syncStateReceiveRequestId = this.duct.nextRid();
        this.$emit(
            'register-sync-state-receive-handler',
            {
                rid: this.syncStateReceiveRequestId,
                handler: async (rid, eid, data) => {
                    let initialSyncState = data;
                    this.initialSpec = initialSyncState.spec;
                    data = await this.duct.call(
                        this.duct.EVENT.NEJI,
                        {
                            genre: this.genre,
                            query: this.shapeQuery,
                        },
                    );

                    for (let [ specKey, specValue ] of Object.entries(data.spec)) {
                        this.selectableItemValues[specKey] = specValue;
                    }

                    let initialQueryKeys = Object.keys(initialSyncState.query);
                    if (initialQueryKeys.includes('中分類')) {
                        this.selectedMiddleClassificationName = initialSyncState.query['中分類'];
                    }
                    if (initialQueryKeys.includes('材質')) {
                        this.selectedMaterialName = initialSyncState.query['材質'];
                    }
                    if (initialQueryKeys.includes('表面処理')) {
                        this.selectedSurfaceName = initialSyncState.query['表面処理'];
                    }
                    if (initialQueryKeys.includes('構成数クラス')) {
                        this.selectedAmountName = initialSyncState.query['構成数クラス'];
                    }
                    if (initialQueryKeys.includes('呼び径')) {
                        this.selectedNominal = initialSyncState.query['呼び径'];
                    }
                    if (initialQueryKeys.includes('外径か幅')) {
                        this.selectedOuter = initialSyncState.query['外径か幅'];
                    }
                    if (initialQueryKeys.includes('長さか厚み')) {
                        this.selectedThickness = initialSyncState.query['長さか厚み'];
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

                    if (Object.keys(data).includes('items')) {
                        this.currentItems = data.items;
                    } else {
                        this.currentItems = null;
                    }

                    this.registerSyncStateReceiveHandler();
                },
            },
        );
    },

    mounted() {
        this.$emit('add-step', 3);
    },

    destroyed() {
        this.$emit(
            'unregister-sync-state-receive-handler',
            { rid: this.syncStateReceiveRequestId },
        );
    },
}
</script>
