<template>
    <v-card tile class="pa-1 ma-1" color="grey lighten-3">
        <v-card-title>{{genre}}の規格を選ぶ</v-card-title>
        <v-card-text> 
            <v-container>
                <v-row>
                    <v-col v-for="(spec, index) in selectableSpec" :key="index" cols="6">
                        <v-menu
                            close-on-content-click
                            transition="scale-transition"
                            offset-y
                        >
                            <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                    v-model="models[index]"
                                    :label="spec.key"
                                    v-bind="attrs"
                                    v-on="on"
                                    outlined
                                    readonly
                                />
                            </template>
                            <v-container style="max-height: 200px" class="ma-0 pa-0">
                                <v-list 
                                    dense
                                >
                                    <v-list-item-group>
                                        <v-list-item
                                            v-for="item in spec.val"
                                            :key="item"
                                            @click="makeQuery(item,spec,index)"
                                        >
                                            <v-list-item-content>
                                                <v-list-item-title>{{item}}</v-list-item-title>
                                            </v-list-item-content>
                                        </v-list-item>
                                    </v-list-item-group>
                                </v-list>
                            </v-container>
                        </v-menu>
                    </v-col>
                </v-row>
            </v-container>
            <v-divider />
            <v-row class="pt-7"> 
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
export default{
    data: () => ({
        isPicked: false,
        initialSpec:{},
        rowSpec:{},
        specQuery:{},
        snackbar:false,
        models:[]
    }),
    props:["duct","genre","shapeQuery"],
    methods: {
        send_query() {
            const _query = Object.assign(this.shapeQuery,this.specQuery);
            this.duct.send(
                this.duct.nextRid(), 
                this.duct.EVENT.NEJI,
                {'genre': this.genre, 'query': _query}
            );
        },
        makeQuery(val,spec,index){
            console.log(index);
            this.models[index] = val;
            this.specQuery[spec.key] = val;
            this.send_query();
        },
        accessNextPage(){
            let _query = Object.assign(this.shapeQuery, this.specQuery)
            if(Object.keys(this.specQuery).length == Object.keys(this.initialSpec).length){
                this.$router.push({
                    name: "FinderResult",
                    params:{ 'totalQuery': _query, 'genre':this.genre }
                });
            }else{
                this.snackbar =true;
            }
        }
    }, 
    computed:{
        formattedInitialSpec(){
            let _arr = Object.entries(this.initialSpec).map(([key,val]) => ({key, val}));
            _arr.forEach((item) => {
                item['val'].sort();
            });
            return _arr
        },
        formattedCurrentSpec(){
            let _arr = Object.entries(this.rowSpec).map(([key,val]) => ({key, val}));
            _arr.forEach((item) => {
                item['val'].sort();
            });
            return _arr
        },
        selectableSpec(){
            let _spec = [];
            for(let index = 0; index < this.models.length; index++){
                if(this.models[index] != null){
                    _spec.push(this.formattedInitialSpec[index]);
                }else{
                    _spec.push(this.formattedCurrentSpec[index]);
                }
            }
            return _spec
        }
    },
    created(){
        this.duct.invokeOnOpen(async () => {
            this.duct.setEventHandler(
                this.duct.EVENT.NEJI,
                (rid, eid, data) => {
                    this.$set(this, 'rowSpec', 'spec' in data ? data.spec : {});
                    if(Object.keys(this.initialSpec).length == 0){
                        this.$set(this, 'initialSpec', 'spec' in data ? data.spec: {});
                        this.models = Array(this.formattedInitialSpec.length);
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
