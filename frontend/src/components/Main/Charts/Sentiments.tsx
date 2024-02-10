import { Analytics } from '@/lib/api/fetchAnalytics'
import { Cell, Legend, Pie, PieChart, ResponsiveContainer } from 'recharts'

type Props = Pick<
	Analytics,
	'total_negatives' | 'total_neutral' | 'total_positives'
>

const COLORS = ['#4ade80', '#60a5fa', '#f87171']

const Sentiments = ({
	total_negatives,
	total_neutral,
	total_positives,
}: Props) => {
	const sentimentData = [
		{ name: 'Positive', value: total_positives },
		{ name: 'Neutral', value: total_neutral },
		{ name: 'Negative', value: total_negatives },
	]
	return (
		<div className='w-72 h-[250px]'>
			<ResponsiveContainer height='100%' width='100%'>
				<PieChart width={400} height={400}>
					<Pie
						dataKey='value'
						isAnimationActive={false}
						data={sentimentData}
						outerRadius={80}
					>
						{sentimentData.map((_, index) => (
							<Cell key={`cell-${index}`} fill={COLORS[index]} />
						))}
					</Pie>
					<Legend />
				</PieChart>
			</ResponsiveContainer>
		</div>
	)
}

export default Sentiments
