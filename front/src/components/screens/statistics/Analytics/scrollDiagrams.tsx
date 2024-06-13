import React from 'react';
// import { Doughnut } from 'react-chartjs-2';
import { PieChart } from '@mui/x-charts/PieChart';
import './scrollDiagramss.css'

// type data = {[{
//   values: any[],
//   label: any[]
// }, 
// ]
// };

function ScrollingCharts({ data }: any) {

  function calculateColor(data: string[]) {
    const numberArr = data.map((i: string) => parseInt(i));
    const minNumber = Math.min(...numberArr);
    const maxNumber = Math.max(...numberArr);
    let colors:string[] = []
  
    numberArr.map((num) => {
      if (num === minNumber)  colors.push("rgba(223, 237, 231, 1)");
      else if (num === maxNumber) colors.push("rgba(240, 229, 227, 1)");
      else return colors.push("rgba(246, 245, 232, 1)");
    });

    return colors
  }
  
  

  return (
    <div className="scroll__diagramms">
      {data.map((item: any) => (
        <div key={item.label}>
          <h5 style={{ display: 'block' }}>{item.label}</h5>
          <PieChart
            series={[
                {
                data: [ { value: item.values[0], color: calculateColor(item.values)[0] },
                        { value: item.values[1], color: calculateColor(item.values)[1] },
                        { value: item.values[2], color: calculateColor(item.values)[2] }
                 ],
                innerRadius: 36,
                outerRadius: 50,
                paddingAngle: -21,
                cornerRadius: 5,
                startAngle: -180,
                endAngle: 180,
                cx: 50,
                cy: 50,
                }
            ]
          }
          height={108}
          width={108}
          slotProps={{
            legend: { hidden: true },
          }}
            />

        </div>
      ))}
    </div>
  );
}

export default ScrollingCharts;
