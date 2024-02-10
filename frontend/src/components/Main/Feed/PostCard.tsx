import { Post } from '@/lib/api/fetchAnalytics'

type Props = {} & Post

const PostCard = (props: Props) => {
	return <>{props.source.name}</>
}

export default PostCard
