const MainLoader = () => {
	return (
		<div className=' flex items-center justify-center flex-col'>
			<img
				src='/team.jpg'
				alt='Loading'
				className='max-h-[450px] mt-24 aspect-square'
			/>
			<p className='text-2xl font-bold mt-8'>
				Please wait for our scraping team to collect the data...
			</p>
		</div>
	)
}

export default MainLoader
