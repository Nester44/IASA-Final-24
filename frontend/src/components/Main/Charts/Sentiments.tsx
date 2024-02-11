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
		<div className='w-[350px] h-[350px]'>
			<ResponsiveContainer height='100%' width='100%'>
				<PieChart>
					<Pie dataKey='value' data={sentimentData} outerRadius={80}>
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