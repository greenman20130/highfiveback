import PropTypes from 'prop-types' // Импортируем PropTypes
import { useState } from 'react'
import './popup.css'

const Popup = ({ notification, notificationText, handleSub }) => {
	const [isVisible, setVisible] = useState(true)

	const handleClick = (e) => {
		e.stopPropagation()
		setVisible(false)
		handleSub((prev) => !prev)
	}
	return (
		<>
			{isVisible && (
				<div className="wrapper--popup" onClick={handleClick}>
					<div className="popup">
						<div className="popup--top">
							<h2>{notification}</h2>
							<p>{notificationText}</p>
						</div>
						<div className="popup--bottom">
							<button className="notification-cancel" onClick={handleClick}>
								Закрыть
							</button>
						</div>
					</div>
				</div>
			)}
		</>
	)
}

Popup.propTypes = {
	notification: PropTypes.string.isRequired,
	notificationText: PropTypes.string.isRequired, // Добавляем проверку для пропса notificationText
	handleSub: PropTypes.func.isRequired,
}

export default Popup
