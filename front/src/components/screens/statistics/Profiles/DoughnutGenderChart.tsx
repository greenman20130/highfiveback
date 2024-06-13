import { styled } from '@mui/material/styles'
import { PieChart, useDrawingArea } from '@mui/x-charts'
import { FC } from 'react'

const data = [
	{ value: 80, label: 'Женщины', color: '#F0E5E3' },
	{ value: 20, label: 'Мужчины', color: '#E2DFED' },
]

const series = [
	{
		data: data,
		innerRadius: 65,
		outerRadius: 100,
		paddingAngle: 0,
		cornerRadius: -1,
		startAngle: -290,
		endAngle: 113,
		cx: 150,
		cy: 150,
	},
]

const StyledText = styled('text')(() => ({
	fill: '#474168CC',
	fontFamily: 'Ubuntu',
	fontWeight: 700,
	textAnchor: 'middle',
	dominantBaseline: 'central',
	fontSize: 40,
}))

function PieCenterLabel({ children }: { children: React.ReactNode }) {
	const { width, height, left, top } = useDrawingArea()
	return (
		<StyledText x={left + width / 2 - 5} y={top + height / 2 - 20}>
			{children}
		</StyledText>
	)
}

const DoughnutGenderChart: FC = () => {
	return (
		<>
			<PieChart
				slotProps={{
					legend: {
						labelStyle: { fill: '#474168', font: 'Raleway' },
						direction: 'column',
						position: { vertical: 'bottom', horizontal: 'left' },
						padding: 50,
					},
				}}
				margin={{ left: 180 }}
				series={series}
			>
				<PieCenterLabel>{data[0].value}%</PieCenterLabel>
			</PieChart>
		</>
	)
}

export default DoughnutGenderChart
