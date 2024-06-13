import React from 'react'
import styles from './DisabledButton.module.css'

const DisabledButton = () => {
	return (
		<div>
			<svg
				className={styles.disabledButton}
				width='39'
				height='39'
				viewBox='0 0 39 39'
				xmlns='http://www.w3.org/2000/svg'
			>
				<g filter='url(#filter0_b_4343_48933)'>
					<rect width='39' height='39' rx='19.5' fillOpacity='0.2' />
					<rect
						x='0.333333'
						y='0.333333'
						width='38.3333'
						height='38.3333'
						rx='19.1667'
						strokeOpacity='0.6'
						strokeWidth='0.666667'
					/>
					<path d='M19.7154 20.764L19.5 20.5485L19.2846 20.764L15.586 24.4625C15.447 24.6016 15.2584 24.6797 15.0617 24.6797C14.8651 24.6797 14.6765 24.6016 14.5375 24.4625C14.3984 24.3235 14.3203 24.1349 14.3203 23.9383C14.3203 23.7416 14.3984 23.553 14.5375 23.414L18.236 19.7154L18.4515 19.5L18.236 19.2846L14.5375 15.586C14.3984 15.447 14.3203 15.2584 14.3203 15.0617C14.3203 14.8651 14.3984 14.6765 14.5375 14.5375C14.6765 14.3984 14.8651 14.3203 15.0617 14.3203C15.2584 14.3203 15.447 14.3984 15.586 14.5375L19.2846 18.236L19.5 18.4515L19.7154 18.236L23.414 14.5375C23.553 14.3984 23.7416 14.3203 23.9383 14.3203C24.1349 14.3203 24.3235 14.3984 24.4625 14.5375C24.6016 14.6765 24.6797 14.8651 24.6797 15.0617C24.6797 15.2584 24.6016 15.447 24.4625 15.586L20.764 19.2846L20.5485 19.5L20.764 19.7154L24.4625 23.414C24.6016 23.553 24.6797 23.7416 24.6797 23.9383C24.6797 24.1349 24.6016 24.3235 24.4625 24.4625C24.3235 24.6016 24.1349 24.6797 23.9383 24.6797C23.7416 24.6797 23.553 24.6016 23.414 24.4625L19.7154 20.764Z' />
				</g>
				<defs>
					<filter
						id='filter0_b_4343_48933'
						x='-16.6667'
						y='-16.6667'
						width='72.3333'
						height='72.3333'
						filterUnits='userSpaceOnUse'
						colorInterpolationFilters='sRGB'
					>
						<feFlood floodOpacity='0' result='BackgroundImageFix' />
						<feGaussianBlur in='BackgroundImageFix' stdDeviation='8.33333' />
						<feComposite
							in2='SourceAlpha'
							operator='in'
							result='effect1_backgroundBlur_4343_48933'
						/>
						<feBlend
							mode='normal'
							in='SourceGraphic'
							in2='effect1_backgroundBlur_4343_48933'
							result='shape'
						/>
					</filter>
				</defs>
			</svg>
		</div>
	)
}

export default DisabledButton
