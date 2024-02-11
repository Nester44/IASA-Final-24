import { SourceId, sources } from '@/components/Header/Header'
import { Post } from '@/lib/api/fetchAnalytics'
import {
	Bar,
	BarChart,
	CartesianGrid,
	Legend,
	ResponsiveContainer,
	Tooltip,
	XAxis,
	YAxis,
} from 'recharts'
type Props = {
	posts: Post[]
}

const mapPostsToData = (posts: Post[]) => {
	const result = []

	const sentimentsBySource: Partial<
		Record<
			SourceId,
			{ negatives: number; neutrals: number; positives: number }
		>
	> = {}

	for (const post of posts) {
		const sourceId = post.source.id

		if (!sentimentsBySource[sourceId]) {
			sentimentsBySource[sourceId] = {
				negatives: 0,
				neutrals: 0,
				positives: 0,
			}
		}

		const sentiment = post.sentiment_rate
		if (sentiment < 0) {
			sentimentsBySource[sourceId]!.negatives++
		} else if (sentiment > 0) {
			sentimentsBySource[sourceId]!.positives++
		} else {
			sentimentsBySource[sourceId]!.neutrals++
		}
	}

	for (const key in sentimentsBySource) {
		const sourceId = key as SourceId
		const a = sentimentsBySource[sourceId]

		if (!a) {
			continue
		}
		const { negatives, neutrals, positives } = a

		result.push({
			sourceId: sources.find((source) => source.id === sourceId)!.name,
			Negative: negatives,
			Neutral: neutrals,
			Positive: positives,
		})
	}

	return result
}

const SourcesTrend = ({ posts }: Props) => {
	const data = mapPostsToData(posts)
	console.log(data)
	return (
		<div className='flex-grow-[1] h-[350px] bg-slate-950'>
			<p className='text-center text-xl font-bold mb-8'>
				Sentiments trend by sources
			</p>
			<ResponsiveContainer width='100%' height='100%'>
				<BarChart
					data={data}
					margin={{
						top: 20,
						right: 30,
						left: 20,
						bottom: 5,
					}}
				>
					<CartesianGrid strokeDasharray='3 3' />
					<XAxis dataKey='sourceId' />
					<YAxis />
					<Tooltip
						wrapperClassName='p-2 rounded-lg border shadow-lg'
						contentStyle={{ background: 'black', border: 'none' }}
					/>
					<Legend />
					<Bar dataKey='Positive' stackId='a' fill='#4ade80' />
					<Bar dataKey='Neutral' stackId='a' fill='#60a5fa' />
					<Bar dataKey='Negative' stackId='a' fill='#f87171' />
				</BarChart>
			</ResponsiveContainer>
		</div>
	)
}

export default SourcesTrend
