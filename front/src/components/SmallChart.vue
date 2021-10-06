<template>
  <v-btn tile height="100%" active-class="aa">
    <div>
      <v-card class="p-3 m-3">
        <v-card-text>
          <highcharts
            :constructorType="'stockChart'"
            class="hc"
            :options="chartOptions"
            ref="priceGraph"
          ></highcharts>
        </v-card-text>
      </v-card>
    </div>
  </v-btn>
</template>

<script>
import { Chart } from "highcharts-vue";
import _ from "lodash";
export default {
  components: {
    highcharts: Chart,
  },
  props: ["data"],
  name: "SmallChart",
  data: function() {
    return {
      chartOptions: {
        chart: {
          height: 200,
          width: 300,
          type: "line",
        },
        credits: false,
        tooltip: { enabled: false },
        navigator: {
          enabled: false,
        },

        rangeSelector: {
          enabled: false,
        },
        yAxis: {
          labels: {
            enabled: false,
          },
          gridLineColor: "transparent",
        },
        xAxis: {
          visible: false,
          labels: {
            enabled: false,
          },
        },
        scrollbar: { enabled: false },
        plotOptions: {
          series: {
            animation: false,
            lineWidth: 1,
            states: {
              hover: {
                enabled: false,
              },
            },
          },
        },
        series: [
          {
            data: this.data,
          },
        ],
      },
    };
  },
  mounted() {
    console.debug("PIZDA", this.data);
  },

  methods: {},
};
</script>
<style scoped>
.aa {
  background: yellow !important;
}
</style>
