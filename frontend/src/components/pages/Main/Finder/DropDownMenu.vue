<template>
    <div>
        <v-row class="pt-5">
            <v-col class="text-body-1">
                {{headerTitle}}を選ぶ
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="6">
                <v-card>
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
                                    v-for="item in inputItems"
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
    methods:{
        emitItem(item){
            this.$emit('update-query', item);
        }
    }
}
</script>
