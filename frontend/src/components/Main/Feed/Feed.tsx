import { Post } from '@/lib/api/fetchAnalytics'
import PostCard from './PostCard'

type Props = {
	posts: Post[]
}

const Feed = ({ posts }: Props) => {
	return (
		<div className='md:columns-2 lg:columns-3 gap-4'>
			{posts.map((post) => (
				<div key={post.id} className='break-inside-avoid mb-4'>
					<PostCard {...post} />
				</div>
			))}
		</div>
	)
}

export default Feed
