import * as React from 'react';
import { BarChart } from '@mui/x-charts/BarChart';
import { within } from '@storybook/test';


//props.wifth: number, props.height: number
//props.data: [[name:string, [value1:number, value2:number, value3:number]], [...], ...]
//rebase: {name: [1, 2, 3], name: [1, 2, 3], name: [1, 2, 3]}

export default function BarsDiagram(props:any) {
  return (
    <BarChart
      series={[
        { data: [3, 4, 1], stack: 'A', label: 'Москва', color: '#dae8e3'},
        { data: [4, 3, 1], stack: 'B', label: 'Санкт-Петербург', color: '#f2f1e1'},
        { data: [4, 2, 5], stack: 'C', label: 'Москва', color:  '#dbd8e8' },

      ]}
      xAxis={[{ scaleType: 'band', data: ['A', 'B', 'C'] }]}
      width={props.width}
      height={props.height}
      grid={{ vertical: true, horizontal: true }}
      slotProps={{
        legend: {
          direction: 'row',
          position: { vertical: 'bottom', horizontal: 'middle' },
          padding: 0,
        },

      }}

      // slots={{
      //   bar: (props) => {
      //     const radius = 7;
      //     const {x, y, height, width, color} = {0, 0, 50, "black"}
        
          
      //     // Path of a rectangle with rounded corners on the right
      //     // for horizontal layout
      //     const d = `M${x},${y} h${width - radius} a${radius},${radius} 0 0 1 ${radius},${radius}v ${height - 2 * radius} a${radius},${radius} 0 0 1 ${-radius},${radius} h${radius - width}z`
      //     return <path d={d} fill={color}
      //     {...restProps} />
      //   }
      // }}
    />
  );
}
