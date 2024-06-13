import { FC } from 'react'
import '../Tabs/Tabs.css'

const ReportDiv: FC = ({ label, children, height, width }) => {
	return (
		<div style={{ width: width, height: height }}>
			<h4 className='div__report__h4' style={{ margin: '2px' }}>
				{label}
			</h4>
			<div className='div__report' style={{ width: width, height: height }}>
				{children}
			</div>
		</div>
	)
}
export default ReportDiv
