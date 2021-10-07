<template>
    <div>
        <v-row class="pt-3">
            <v-col>
                <v-card dark flat color="#424242">
                    <span class="text-subtitle-1 d-flex justify-center">{{headerTitle}}を選ぶ</span>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="6">
                <v-card max-width="200" class="mx-auto">
                <v-img
                    :src="imageSource"
                />
                </v-card>
            </v-col>
            <v-col cols="6">
                <v-menu
                    close-on-content-click
                    transition="scale-transition"
                    offset-y
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="model"
                            :label="headerTitle"
                            v-bind="attrs"
                            v-on="on"
                            outlined
                            readonly
                            append-icon="mdi-menu-down"
                            dense
                        />
                    </template>
                    <v-container style="max-height: 200px" class="ma-0 pa-0">
                        <v-list 
                            dense
                        >
                            <v-list-item-group>
                                <v-list-item
                                    v-for="item in inputItemsSorted"
                                    :key="item.val"
                                    @click="emitItem(item)"
                                >
                                    <v-list-item-content>
                                        <v-list-item-title>
                                            {{item.val}}
                                        </v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list-item-group>
                        </v-list>
                    </v-container>
                </v-menu>
            </v-col>
        </v-row>
    </div>
</template>
<script>
export default{
    props:["headerTitle","imageSource","model","inputItems"],
    computed: {
        inputItemsSorted() {
            return this.inputItems
                .map((item) => ({ name: item.name, val: item.val, sortValue: this.convertToFloatOrLargeNumber(item.val) }))
                .sort((a,b) => (a.sortValue>b.sortValue ? 1 : -1));
        }
    },
    methods:{
        convertToFloatOrLargeNumber(str) {
            if(typeof(str)=='number') str = str.toString();
            let _str = str.replace(/[０-９]/g, (s) => (String.fromCharCode(s.charCodeAt(0) - 0xFEE0)))
                .replace('．', '.')
                .replace('／', '/');
            if(/^[0-9./]+$/.test(_str)) {
                let nums = _str.split('/').map((c) => parseFloat(c));
                if(nums.length==2) nums[0] /= nums[1];
                return nums[0];
            } else {
                return 99999;
            }
        },
        emitItem(item){
            this.$emit('update-query', item);
        }
    },
    //watch: {
    //    inputItemsSorted() {
    //        console.log(this.inputItemsSorted);
    //    }
    //}
}
</script>
