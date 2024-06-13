import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import { useDrawingArea } from '@mui/x-charts/hooks';
import { styled } from '@mui/material/styles';
import './PieChartWithLabel.css'

const COLORS = ["#0088FE", "#03C39F", "#FFB827", "#FE8042"];
const getColor = (index: number) => COLORS[index % COLORS.length];

const data = [
  { value: 5, label: 'A' },
  { value: 10, label: 'B' },
  { value: 15, label: 'C' },
  { value: 20, label: 'D' },
];

const size = {
  width: 400,
  height: 200,
};

const StyledText = styled('text')(({ theme }) => ({
  fill: theme.palette.text.primary,
  textAnchor: 'middle',
  dominantBaseline: 'central',
  fontSize: 20,
}));

function PieCenterLabel({ children }: any) {
  const { width, height, left, top } = useDrawingArea();
  return (
    <StyledText x={left + width / 2} y={top + height / 2}>
      {children}
    </StyledText>
  );
}

//props.data
//props.label
export default function PieChartWithLabel(props: any) {
  const { data, label, width, height } = props;

  return (
    <PieChart series={[{data, innerRadius: 55, outerRadius: 78 }]} width={width} height={height}
      margin={{ 'bottom': 90, 'left': 5, 'right': 0 }}
        slotProps={{
          legend: {
            direction: 'column',
            position: { vertical: 'bottom', horizontal: 'middle' },
            padding: -10,
            labelStyle: {
              fontSize: 9,
              fill: '#474168',
            },
          },
        }}>

      <PieCenterLabel>{label +"%"}</PieCenterLabel>
        {/*  */}
        {/*  */}
    </PieChart>
  );
}