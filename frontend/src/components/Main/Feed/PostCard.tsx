import { sources } from '@/components/Header/Header'
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card'
import { Post } from '@/lib/api/fetchAnalytics'

type Props = {} & Post

const PostCard = ({ content, created, sentiment_rate, source, url }: Props) => {
	const iconSrc = sources.find((s) => s.id === source.id)?.iconSrc
	return (
		<Card className='flex flex-col overflow-hidden'>
			<CardHeader>
				<div className='flex justify-between'>
					<a href={url} className='flex gap-4' target='_blank'>
						<img
							src={iconSrc}
							alt='twitter'
							className='w-8 h-8 rounded'
						/>
						<p className='text-lg font-bold'>{source.name}</p>
					</a>
					<Sentiment sentiment_rate={sentiment_rate} />
				</div>
			</CardHeader>
			<CardContent className='flex-grow'>
				<p>
					{content.length > 255
						? `${content.slice(0, 255)}...`
						: content}
				</p>
			</CardContent>

			<CardFooter>
				<p className='text-sm ml-auto  text-gray-500'>
					{new Date(created * 1000).toLocaleString()}
				</p>
			</CardFooter>
		</Card>
	)
}

export default PostCard

function Sentiment({ sentiment_rate }: { sentiment_rate: number }) {
	return (
		<p
			className={`font-bold ${
				sentiment_rate > 0
					? 'text-green-500'
					: sentiment_rate < 0
					? 'text-red-500'
					: 'text-gray-500'
			}`}
		>
			{sentiment_rate > 0
				? 'Positive'
				: sentiment_rate < 0
				? 'Negative'
				: 'Neutral'}
		</p>
	)
}
