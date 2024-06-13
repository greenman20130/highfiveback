import React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
// import './scrollDiagramss.css'
import { ChartContainer } from '@mui/x-charts';
import { areaElementClasses, LineChart } from '@mui/x-charts/LineChart';
import {
  LinePlot,
  MarkPlot,
  lineElementClasses,
  markElementClasses,
} from '@mui/x-charts/LineChart';

const uData = [4000, 3000, 2000, 2780, 1890, 2390];
const pData = [2400, 1398, 9800, 3908, 4800, 3800];
const wData = [240, 198, 980, 208, 4400, 800];


// props.data: numbers[]


export default function LinearChart(props:any) {

  function generateMouth(now:string, count:number){
    const months = [
      "Январь", "Февраль", "Март",
      "Апрель", "Май", "Июнь",
      "Июль", "Август", "Сентябрь",
      "Октябрь", "Ноябрь", "Декабрь"
    ];
    const startIndex = months.indexOf(now);
    // if (startIndex === -1) {
    //   return "Ошибка: Введен некорректный месяц";
    // }
  
    const resultMonths = [];
    let currentMonthIndex = startIndex;
  
    for (let i = 0; i < count; i++) {
      resultMonths.push(months[currentMonthIndex]);
      currentMonthIndex = (currentMonthIndex + 1) % 12;
    }
  
    return resultMonths;
  }

  const xLabels = generateMouth('Январь', 6)

  return (
    <LineChart
      width={props.width}
      height={props.height}
      series={[{
        // data: [{ data: pData, label: 'месяц', area: true },
        // { data: uData, label: 'уровень выгорания' }],
        data: pData,
        color: "rgba(209, 85, 65)",
        label: "Москва"
      },
    {
        data: uData,
        color: "#dbd8e8",
        label: "Москва"

    },
    {
      data: wData,
      color: "rgba(223, 237, 231, 1)",
      label: "Казань"


  }]}
      xAxis={[{ scaleType: 'point', data: xLabels }]}
      grid={{ vertical: true, horizontal: true }}
      sx={{
        // [`& .${lineElementClasses.root}`]: {
        //   stroke: 'red',
        //   strokeWidth: 2,
        // },
        [`& .${markElementClasses.root}`]: {
          stroke: 'grey',
          scale: '0.6',
          fill: '#fff',
          strokeWidth: 2,
        },
        [`& .${areaElementClasses.root}`]: {
          fill: ['rgba(209, 85, 65, .3)'],
        }
      }}
      slotProps={{
        legend: {
          labelStyle: {
            fontSize: 8,
            fill: 'black',
          },
          direction: 'row',
          position: { vertical: 'bottom', horizontal: 'middle' },
          padding: 0,
        },
      }}
    />
  );
}
