import { Analytics } from '@/lib/api/fetchAnalytics'
import WordCloud from 'react-d3-cloud'

type Props = {} & Pick<Analytics, 'keywords'>

const Cloud = ({ keywords }: Props) => {
	const data = keywords.map(([text, value]) => ({ text, value: 1 / value }))

	return (
		<div className=' overflow-hidden mb-8 relative'>
			<WordCloud
				data={data}
				height={300}
				font='ui-sans-serif'
				fontWeight='bold'
				fontSize={(word) => Math.log2(word.value) * 2}
				padding={1}
				random={Math.random}
				fill={(_: any, i: number) => {
					const colors = [
						'#4ade80',
						'#60a5fa',
						'#f87171',
						'#fbbf24',
						'#818cf8',
						'#34d399',
						'#f472b6',
						'#6ee7b7',
						'#93c5fd',
						'#fbbf24',
					]
					return colors[i % colors.length]
				}}
			/>
		</div>
	)
}

export default Cloud
