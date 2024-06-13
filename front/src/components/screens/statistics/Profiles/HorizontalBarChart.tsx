import { BarChart } from '@mui/x-charts'
import { FC } from 'react'

const data = [
	{ data: 88, age: 'До 35 лет' },
	{ data: 60, age: 'От 35 лет' },
]

const series = [
	{
		dataKey: 'data',
	},
]

const HorizontalBarChart: FC = () => {
	return (
		<BarChart
			yAxis={[
				{
					scaleType: 'band',
					dataKey: 'age',
					colorMap: { type: 'ordinal', colors: ['#DFEDE7', '#E2DFED'] },
				},
			]}
			series={series}
			margin={{ top: 30, left: 70 }}
			dataset={data}
			layout='horizontal'
			width={600}
			height={170}
		/>
	)
}

export default HorizontalBarChart
