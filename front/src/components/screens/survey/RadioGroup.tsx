import { Radio, RadioChangeEvent, Space } from 'antd'
import { FC, useState } from 'react'
import styles from './Survey.module.css'
import './radioStyle.css'
import { IOption } from './types/ITemplate'

interface IRadioGroupProps {
	options: IOption[]
	radioAnswer: (answer: string) => void
}

const RadioGroup: FC<IRadioGroupProps> = ({ options, radioAnswer }) => {
	const [checked, setChecked] = useState<string | null>(null)

	const onChange = (e: RadioChangeEvent) => {
		setChecked(e.target.value)
		const result: string = e.target.value
		radioAnswer(result)
	}

	return (
		<div className={styles.innerQuestion}>
			<Radio.Group onChange={onChange} value={checked}>
				<Space direction="vertical">
					{options.map((item) => (
						<Radio
							key={item.id}
							style={{ color: '#474168', fontSize: '20px' }}
							value={item.id}
						>
							{item.value}
						</Radio>
					))}
				</Space>
			</Radio.Group>
		</div>
	)
}
export default RadioGroup
