import React from 'react'
import { IconContext } from 'react-icons'
import * as MaterialIcons from 'react-icons/pi'
import { useRenderClient } from '../../hooks/useRenderClient'

const MaterialIcon = ({ icon }) => {
	const { isRenderClient } = useRenderClient()

	const IconComponent = MaterialIcons[icon]

	if (isRenderClient)
		return (
			<IconContext.Provider
				value={{ size: '25px', className: 'global-class-name' }}
			>
				<IconComponent />
			</IconContext.Provider>
		)
	else return null
}

export default MaterialIcon
