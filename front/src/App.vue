<template>
  <v-app>
    <v-app-bar app height=350>

      <v-card elevation="4" v-if="newPrice">
        <v-card-title>
          <span>Текущая цена портфеля:</span>
        </v-card-title>
        <v-card-text class="text-h5 font-weight-bold">
          <h2>
            <v-icon x-large :color="direction.color">{{
              direction.icon
              }}
            </v-icon>

            {{ tweenedPrice || newPrice }}
          </h2>
        </v-card-text>
      </v-card>
      <v-card elevation="4" v-if="currentROR" class="mx-3">
        <v-card-title>
          <span>Текущая доходность:</span>
        </v-card-title>
        <v-card-text class="text-h5 font-weight-bold">
          <h2>
            <v-icon x-large :color="direction.color">{{
              direction.icon
              }}
            </v-icon>

            {{ parseFloat(currentROR * 100).toFixed(2) }}%
          </h2>
        </v-card-text>
      </v-card>
      <v-card v-if="false">
        <v-card-text>
          <v-btn @click="showDialog">Sell</v-btn>
        </v-card-text>
      </v-card>
      <v-card elevation="4" v-if="true">
        <v-card-title>Довольны результатом? Переместите слайдер вправо (макс 100). Недовольны - влево (мин.0).
        </v-card-title>
        <v-card-text>
          <div>
            Если хотите продать портфель до срока, переместите слайдер влево до упора (на 0). Вас попросят
            подтвердить решение.
          </div>
          <div class="d-flex align-items-center justify-center my-3">
            <round-slider
                rangeColor="green"
                v-model="sliderValue"
                start-angle="315"
                end-angle="+270"
                line-cap="round"
                :valueChange="changeslider"
            />
          </div>
        </v-card-text>
      </v-card>
    </v-app-bar>
    <v-dialog v-model="dialog" max-width="600">
      <v-card>
        <v-card-title class="text-h5"> Решение о продаже</v-card-title>

        <v-card-text>
          Вы хотите продать портфель? Если Вы выберете "продать", период закончится.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="green darken-1" @click="continueKeeping">
            Оставить
          </v-btn>

          <v-btn color="red darken-1" @click="sell"> Продать</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-main>
      <v-container fluid>

        <v-row>
          <v-col cols="12"
          >
            <highcharts
                :constructorType="'stockChart'"
                class="hc"
                :options="chartOptions"
                ref="chart1"
                :updateArgs="[true, true, true]"
            ></highcharts
            >

          </v-col>


        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
/* eslint-disable */

import RoundSlider from "vue-round-slider";
import {Chart} from "highcharts-vue";

import gsap from "gsap";
import _ from "lodash";

const firstOne = window.data[0]
const ror = _.map(window.data, (i) => (i - firstOne) / firstOne)

const formatDown = {
  color: "red",
  icon: "mdi-arrow-down-bold",
};
const formatUp = {
  color: "green darken-3",
  icon: "mdi-arrow-up-bold",
};

export default {
  name: "App",
  components: {
    highcharts: Chart,
    RoundSlider,
  },
  data: function () {
    const chunkSize = 10
    const firstVal = window.data.slice(0, chunkSize);
    const rorFirstVal = ror.slice(0, chunkSize)
    return {
      currentROR: (_.last(firstVal) - window.data[0]) / window.data[0],
      newPrice: window.data[0],
      previousPrice: window.data[0],
      sliderColor: null,
      dialog: false,
      sliderValue: 100,
      tweenedPrice: null,
      counter: 0,
      chunkSize,
      stockIntervall: null,
      tickFrequency: 3,
      chartOptions: {
        xAxis: {
          max: window.data.length,
          ordinal: false,
          plotBands: [
            {
              borderColor: "red",
              borderWidth: 1,
              color: "#FCFFC5", // Color value
              from:0,
              to: null
            },
          ]
        },
        yAxis: {
          min: window.data[0] - (window.data[0] - window.drawdown) * 2,
          plotLines: [{
            value: window.drawdown,
            color: 'red',
            width: 2,
            dashStyle: 'shortdash'
          }]
        },
        navigator: {enabled: false},
        rangeSelector: {
          inputEnabled: false,
          selected: false,
        },
        series: [
          {
            data: firstVal,
          },
        ],
      }
    };
  },
  computed: {
    direction() {
      if (this.currentPrice > this.previousPrice) {
        return formatUp;
      } else {
        return formatDown;
      }
    },


  },
  watch: {
    sliderValue(val) {

      if (val === 0) {
        this.dialog = true;
      }
    },
    newPrice: function (newValue) {
      console.debug('do we reach the watcher')
      gsap.to(this.$data, {
        duration: 0.5,
        tweenedPrice: newValue,
      });
    },
  },
  mounted() {
    this.stockInterval = setInterval(() => {
      const newCounter = this.counter + this.chunkSize
      this.newPrice = window.data[newCounter]
      const oldCounter = this.counter
      this.currentROR = (this.newPrice - window.data[0]) / window.data[0]
      this.previousPrice = window.data[this.counter]

      const newData = window.data.slice(this.counter, newCounter);
      this.counter += this.chunkSize;

      if (this.newPrice) {
          this.chartOptions.series[0].data.push(...newData);
        this.chartOptions.xAxis.plotBands[0].from=oldCounter+this.chunkSize
        this.chartOptions.xAxis.plotBands[0].to=newCounter+this.chunkSize


      } else document.getElementById("form").submit();
    }, this.tickFrequency * 1000);
  },
  methods: {
    showDialog() {
      this.dialog=true
    },
    changeslider(v) {
    },
    continueKeeping() {
      this.sliderValue = 100;
      this.dialog = false;
    },
    sell() {
      this.dialog = false;
      document.getElementById("form").submit();
    },
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
