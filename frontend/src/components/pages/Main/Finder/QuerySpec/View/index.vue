<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の規格を選ぶ</v-card-title>
        <v-card-text> 
            <v-btn
                @click="resetQuery"
            >
                規格をリセットする
            </v-btn>
            <card-button 
                :headerIsOn="true"
                headerTitle="材質"
                :inputItems="selectableMaterial"
                @update-query="makeQuery"
                :labelIsOn="false"
            />
            <v-divider />
            <v-slide-y-transition>
                <card-button 
                    :headerIsOn="true"
                    headerTitle="表面処理"
                    :inputItems="selectableSurface"
                    @update-query="makeQuery"
                    :labelIsOn="false"
                />
            </v-slide-y-transition>
            <v-divider />
            <v-slide-y-transition>
                <card-button 
                    :headerIsOn="true"
                    headerTitle="構成数クラス"
                    :inputItems="selectableAmount"
                    @update-query="makeQuery"
                    :labelIsOn="false"
                />
            </v-slide-y-transition>
            <v-divider />
            <v-slide-y-transition>
                    <drop-down-menu
                        headerTitle="呼び径"
                        :imageSource="nominal.image"
                        :model="nominal.model"
                        :inputItems="selectableNominal"
                        @update-query="makeQuery"
                    />
            </v-slide-y-transition>
            <v-divider />
            <v-slide-y-transition>
                    <drop-down-menu
                        v-if="outer.isNecessary"
                        headerTitle="外径・幅"
                        :imageSource="outer.image"
                        :model="outer.model"
                        :inputItems="selectableOuter"
                        @update-query="makeQuery"
                    />
            </v-slide-y-transition>
            <v-divider />
            <v-slide-y-transition>
                    <drop-down-menu
                        v-if="thickness.isNecessary"
                        headerTitle="長さ・厚さ"
                        :imageSource="thickness.image"
                        :model="thickness.model"
                        :inputItems="selectableThickness"
                        @update-query="makeQuery"
                    />
            </v-slide-y-transition>
            <v-divider />
            <v-row v-if="itemQuantity != 0" class="pt-5">
                <v-col>
                    該当商品数：{{itemQuantity}}個
                </v-col>
            </v-row>
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
                <v-btn
                    dark
                    :disabled="buttonDisabled"
                    color="primary"
                    @click="accessNextPage"
                >
                    次に進む 
                    <v-icon>mdi-arrow-right</v-icon>
                </v-btn>  
            </v-row>
        </v-card-text>   
        <v-snackbar
            v-model="snackbar"
            timeout="2000"
        >選択されていない項目があります
        </v-snackbar>
    </v-card>
</template>
<script>
import { icons } from '../../spec_profile.js'
import CardButton from '../../CardButton'
import DropDownMenu from '../../DropDownMenu'
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
        DropDownMenu
    },
    data: () => ({
        icons,
        specQuery:{},
        
        snackbar:false,
        initialSpec:{},
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
        pickedMaterial:[],
        pickedSurface:[],
        pickedAmount:[],
        pickedNominal:[],
        pickedOuter:[],
        pickedThickness:[],
        itemQuantity:0,
        buttonDisabled:true,
        currentItems:[],

    }),
    props:["duct","genre","shapeQuery"],
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
            if(this.icons.material.includes(item)){
                this.specQuery = {};
                this.specQuery["材質"] = item.name;
                changeBackgroundColor(item, this.icons.material);
                this.send_query();
            }else if(this.icons.surface.includes(item)){
                this.specQuery["表面処理"] = item.name;
                changeBackgroundColor(item, this.icons.surface);
                this.send_query();
            }else if(this.icons.amount.includes(item)){
                this.specQuery["構成数クラス"] = item.name;
                changeBackgroundColor(item, this.icons.amount);
                this.send_query();
            }else if(this.initialSpec["呼び径"].includes(item.val) && item.name=="呼び径" ){
                this.specQuery["呼び径"] = item.val;
                this.nominal.model = item.val; 
                this.send_query();
            }else if(this.outer.isNecessary && this.initialSpec["外径か幅"].includes(item.val) && item.name=="外径か幅" ){
                this.specQuery["外径か幅"] = item.val;
                this.outer.model = item.val; 
                this.send_query();
            }else if(this.thickness.isNecessary && this.initialSpec["長さか厚み"].includes(item.val) && item.name=="長さか厚み"){
                this.specQuery["長さか厚み"] = item.val;
                this.thickness.model = item.val; 
                this.send_query();
            }
        },
        resetQuery(){
            this.specQuery = {};
            this.send_query();
            changeBackgroundColor({ name: "" }, this.icons.material);
            changeBackgroundColor({ name: "" }, this.icons.surface);
            changeBackgroundColor({ name: "" }, this.icons.amount);
            this.nominal.model="";
            this.outer.model="";
            this.thickness.model="";
        },
        accessNextPage(){
            const _query = {}
            Object.assign(_query, this.shapeQuery,this.specQuery)
            if(this.itemQuantity == 1){
                this.$router.push({
                    name: "FinderResult",
                    params:{ 'item': this.currentItems }
                });
            }else{
                this.$router.push({
                    name: "ResultList",
                    params:{ 'items': this.currentItems }
                });
            }
        }
    }, 
    watch:{
        itemQuantity(){
            if (this.itemQuantity != 0){
                this.buttonDisabled = false;
            }else{
                this.buttonDisabled = true;
            }
        }
    },
    computed:{
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


        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {
                    console.log(data);
                    if(Object.keys(this.specQuery).length == 0){
                        this.initialSpec = data.spec
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
                    }
                }
            )
            this.send_query();
        });
    },
    mounted(){
        this.$emit('add-step', 3);
    }
}
</script>
