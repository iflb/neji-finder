<template>
    <v-stepper 
        v-model="stepper" 
        alt-labels
        flat 
    >
        <v-stepper-header>
            <v-stepper-step
                :complete="stepper > 1"
                step="1"
            >ジャンル決定
            </v-stepper-step>
            <v-divider />
            <v-stepper-step
                :complete="stepper > 2"
                step="2"
            >形状決定
            </v-stepper-step>
            <v-divider />
            <v-stepper-step
                :complete="stepper > 3"
                step="3"
            >規格決定
            </v-stepper-step>
            <v-divider />
            <v-stepper-step
                :complete="stepper > 4"
                color="#EF5350"
                step="4"
            >商品確定
            </v-stepper-step>
        </v-stepper-header>
    </v-stepper>
</template>
<script>
export default{
    props:["stepper"]
}
</script>
