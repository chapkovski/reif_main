<template>
  <v-card width="100%" height="150">
    <v-subheader
      >Переместите слайдер в зависимости от вашего желания продать или держать
      акции</v-subheader
    >

    <v-card-text>
      <v-slider
        v-model="sellingDecision"
        :tick-labels="ticksLabels"
        :max="3"
        step="1"
        ticks="always"
        tick-size="20"
        :thumb-size="70"
        @change="changeSliderValue"
      >
        <template v-slot:thumb-label="{ value }">
          <div class="text-center">{{ ticksLabels[value] }}</div>
        </template>
      </v-slider>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ["reset"],
  data: () => ({
    sellingDecision: 3,
    ticksLabels: ["Продать", "Скорее продать", "Скорее держать", "Держать"],
  }),
  watch: {
    reset(newV, oldV) {
      if (!newV && oldV) {
        this.sellingDecision = 3;
      }
    },
  },
  methods: {
    changeSliderValue(value) {
      this.$emit("sliderValChange", value);
    },
  },
};
</script>
<style>
.v-slider__tick {
  background: red !important;
}
</style>
<style lang="sass">
$slider-tick-border-radius:10
</style>
