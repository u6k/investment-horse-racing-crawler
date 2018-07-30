require 'test_helper'

class RaceListPageTest < ActiveSupport::TestCase

  def setup
    @bucket = NetModule.get_s3_bucket
    @bucket.objects.batch_delete!
  end

  # test "download race list page" do
  #   # precondition
  #   course_list_page = CourseListPage.download(2018, 7, 16)
  #   course_list_page.save!

  #   # execute 1
  #   race_list_pages = course_list_page.download_race_list_pages

  #   # postcondition 1
  #   assert_equal 5, race_list_pages.length

  #   race_list_page = race_list_pages[0]
  #   assert_equal "帯広競馬場", race_list_page.course_name
  #   assert_equal "ナイター", race_list_page.timezone
  #   assert_equal "https://www.oddspark.com/keiba/OneDayRaceList.do?raceDy=20180716&opTrackCd=03&sponsorCd=04", race_list_page.url
  #   assert race_list_page.content.length > 0
  #   assert race_list_page.course_list_page.same?(course_list_page)
  #   assert race_list_page.valid?
  #   assert_not @bucket.object("race_list/20180716/帯広競馬場/race_list.html").exists?

  #   race_list_page = race_list_pages[1]
  #   assert_equal "盛岡競馬場", race_list_page.course_name
  #   assert_equal "薄暮", race_list_page.timezone
  #   assert_equal "https://www.oddspark.com/keiba/OneDayRaceList.do?raceDy=20180716&opTrackCd=11&sponsorCd=06", race_list_page.url
  #   assert race_list_page.content.length > 0
  #   assert race_list_page.course_list_page.same?(course_list_page)
  #   assert race_list_page.valid?
  #   assert_not @bucket.object("race_list/20180716/盛岡競馬場/race_list.html").exists?

  #   race_list_page = race_list_pages[2]
  #   assert_equal "名古屋競馬場", race_list_page.course_name
  #   assert_equal "", race_list_page.timezone
  #   assert_equal "https://www.oddspark.com/keiba/OneDayRaceList.do?raceDy=20180716&opTrackCd=43&sponsorCd=33", race_list_page.url
  #   assert race_list_page.content.length > 0
  #   assert race_list_page.course_list_page.same?(course_list_page)
  #   assert race_list_page.valid?
  #   assert_not @bucket.object("race_list/20180716/金沢競馬場/race_list.html").exists?

  #   race_list_page = race_list_pages[3]
  #   assert_equal "高知競馬場", race_list_page.course_name
  #   assert_equal "ナイター", race_list_page.timezone
  #   assert_equal "https://www.oddspark.com/keiba/OneDayRaceList.do?raceDy=20180716&opTrackCd=55&sponsorCd=29", race_list_page.url
  #   assert race_list_page.content.length > 0
  #   assert race_list_page.course_list_page.same?(course_list_page)
  #   assert race_list_page.valid?
  #   assert_not @bucket.object("race_list/20180716/高知競馬場/race_list.html").exists?

  #   race_list_page = race_list_pages[4]
  #   assert_equal "佐賀競馬場", race_list_page.course_name
  #   assert_equal "薄暮", race_list_page.timezone
  #   assert_equal "https://www.oddspark.com/keiba/OneDayRaceList.do?raceDy=20180716&opTrackCd=61&sponsorCd=30", race_list_page.url
  #   assert race_list_page.content.length > 0
  #   assert race_list_page.course_list_page.same?(course_list_page)
  #   assert race_list_page.valid?
  #   assert_not @bucket.object("race_list/20180716/佐賀競馬場/race_list.html").exists?

  #   assert_equal 1, CourseListPage.all.length
  #   assert_equal 0, RaceListPage.all.length

  #   # execute 2
  #   race_list_pages.each do |race_list_page|
  #     race_list_page.save!
  #   end

  #   # postcondition 2
  #   assert_equal 5, RaceListPage.all.length

  #   course_list_page.race_list_pages.each do |race_list_page_db|
  #     race_list_page = race_list_pages.find { |i| i.url == race_list_page_db.url }

  #     assert race_list_page.same?(race_list_page_db)
  #   end

  #   assert @bucket.object("race_list/20180716/帯広競馬場/race_list.html").exists?
  #   assert @bucket.object("race_list/20180716/盛岡競馬場/race_list.html").exists?
  #   assert @bucket.object("race_list/20180716/名古屋競馬場/race_list.html").exists?
  #   assert @bucket.object("race_list/20180716/高知競馬場/race_list.html").exists?
  #   assert @bucket.object("race_list/20180716/佐賀競馬場/race_list.html").exists?

  #   # execute 3
  #   race_list_pages_2 = course_list_page.download_race_list_pages

  #   # postcondition 3
  #   assert_equal 5, RaceListPage.all.length

  #   race_list_pages_2.each do |race_list_page_2|
  #     assert_not_nil race_list_page_2.id
  #     assert race_list_page_2.content.length > 0
  #     assert race_list_page_2.valid?
  #   end

  #   # execute 4
  #   race_list_pages_2.each do |race_list_page_2|
  #     race_list_page_2.save!
  #   end

  #   # postcondition 4
  #   assert_equal 5, RaceListPage.all.length
  # end

  # test "download race list page: invalid html" do
  #   # precondition
  #   course_list_page = CourseListPage.download(2018, 7, 16)
  #   course_list_page.save!

  #   # execute 1
  #   race_list_page = RaceListPage.download(course_list_page, "aaa", "bbb", "https://www.oddspark.com/keiba/OneDayRaceList.do?raceDy=19000101&opTrackCd=01&sponsorCd=01")

  #   # postcondition 1
  #   assert race_list_page.content.length > 0
  #   assert race_list_page.invalid?
  #   assert_equal "Invalid html", race_list_page.errors[:course_name][0]

  #   assert_equal 0, RaceListPage.all.length

  #   assert_not @bucket.object("race_list/19000101/aaa/race_list.html").exists?

  #   # execute 2
  #   assert_raise ActiveRecord::RecordInvalid, "Course name Invalid html" do
  #     race_list_page.save!
  #   end

  #   # postcondition 2
  #   assert_equal 0, RaceListPage.all.length

  #   assert_not @bucket.object("race_list/19000101/aaa/race_list.html").exists?
  # end

  # test "find all" do
  #   # precondition
  #   course_list_page = CourseListPage.download(2018, 7, 16)
  #   course_list_page.save!

  #   race_list_pages = course_list_page.download_race_list_pages
  #   race_list_pages.each { |r| r.save! }

  #   # execute
  #   race_list_pages_2 = course_list_page.race_list_pages

  #   # postcondition
  #   assert_equal race_list_pages.length, race_list_pages_2.length

  #   race_list_pages.each do |race_list_page|
  #     race_list_page_2 = race_list_pages_2.find { |r| r.course_name == race_list_page.course_name }

  #     assert race_list_page.same?(race_list_page_2)
  #   end
  # end

  # test "parse" do
  #   # precondition
  #   course_list_page = CourseListPage.download(2018, 7, 16)
  #   course_list_page.save!

  #   race_list_pages = course_list_page.download_race_list_pages
  #   race_list_pages.each { |r| r.save! }

  #   # execute
  #   entry_list_pages = race_list_pages[0].download_entry_list_pages
  #   refund_list_page = race_list_pages[0].download_refund_list_page

  #   # postcondition
  #   assert_equal 11, entry_list_pages.length
  #   entry_list_pages.each { |e| assert e.valid? }

  #   assert refund_list_page.valid?

  #   assert_equal 0, EntryListPage.all.length
  #   assert_equal 0, RefundListPage.all.length
  # end

end
