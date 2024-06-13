import { styled } from '@mui/material/styles'
import { PieChart, useDrawingArea } from '@mui/x-charts'
import { FC } from 'react'

const data = [
	{ value: 95, color: '#FDFBFB' },
	{ value: 5, color: '#DFEDE7' },
]

const series = [
	{
		data: data,
		innerRadius: 60,
		outerRadius: 50,
		cornerRadius: -1,
		cx: 80,
		cy: 55,
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
		<StyledText x={left + width / 2 + 50} y={top + height / 2 - 5}>
			{children}
		</StyledText>
	)
}

const DoughnutBurnoutChart: FC = () => {
	return (
		<>
			<PieChart series={series}>
				<PieCenterLabel>{data[1].value}%</PieCenterLabel>
			</PieChart>
		</>
	)
}

export default DoughnutBurnoutChart
