import { ArcElement, Chart as ChartJS, Legend, Tooltip } from 'chart.js'
import { FC } from 'react'
import { Doughnut } from 'react-chartjs-2'
import styles from './GeneralInfo.module.css'

ChartJS.register(ArcElement, Tooltip, Legend)

const data = {
	labels: ['Высокая тяжесть показателей', 'Отклонений нет'],
	datasets: [
		{
			data: [20, 80],
			backgroundColor: ['rgba(209, 85, 65, 0.4)', 'rgba(255, 255, 255, 1)'],
			borderColor: ['rgba(209, 85, 65, 1)', 'rgba(255, 255, 255, 1)'],
			borderWidth: 1,
			borderRadius: 50,
		},
	],
}

const DoughnutChart: FC = () => {
	return (
		<>
			<Doughnut
				data={data}
				options={{
					plugins: {
						legend: {
							position: 'bottom',
							align: 'start',
							labels: { boxWidth: 11, font: { family: 'Raleway' } },
						},
					},
					cutout: 75,
				}}
			/>
			<span className={styles.percent}>{data.datasets[0].data[0]}%</span>
		</>
	)
}

export default DoughnutChart
