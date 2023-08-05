#include "opennurbs.h"

#if !defined(ON_COMPILING_OPENNURBS)
// This check is included in all opennurbs source .c and .cpp files to insure
// ON_COMPILING_OPENNURBS is defined when opennurbs source is compiled.
// When opennurbs source is being compiled, ON_COMPILING_OPENNURBS is defined 
// and the opennurbs .h files alter what is declared and how it is declared.
#error ON_COMPILING_OPENNURBS must be defined when compiling opennurbs
#endif

#include "opennurbs_subd_data.h"

#if defined(OPENNURBS_SUBD_WIP)


bool ON_SubDQuadNeighborhood::IsValid() const
{
  unsigned int count = 0;
  for (unsigned int i = 0; i < 4; i++)
  {
    if (m_bExtraordinaryCornerVertex[i])
      count++;
  }
  if (count != m_extraordinary_corner_vertex_count)
    return ON_SUBD_RETURN_ERROR(false);

  count = 0;
  for (unsigned int i = 0; i < 4; i++)
  {
    if (m_bExactQuadrantPatch[i])
    {
      if (m_bExtraordinaryCornerVertex[i] )
        return ON_SUBD_RETURN_ERROR(false);
      count++;
    }
  }
  if (count != m_exact_quadrant_patch_count)
    return ON_SUBD_RETURN_ERROR(false);

  count = 0;
  for (unsigned int i = 0; i < 4; i++)
  {
    if (m_bBoundaryCrease[i])
    {
      //if ( m_bDartCrease[i] )
      //  return ON_SUBD_RETURN_ERROR(false);
      count++;
    }
  }
  if (count != m_boundary_crease_count)
    return ON_SUBD_RETURN_ERROR(false);

  //count = 0;
  //for (unsigned int i = 0; i < 4; i++)
  //{
  //  if (m_bDartCrease[i])
  //    count++;
  //}
  //if (count != m_dart_crease_count)
  //  return ON_SUBD_RETURN_ERROR(false);

  const ON_SubDFace* quad_face = m_face_grid[1][1];
  if (nullptr == quad_face || 4 != quad_face->m_edge_count)
    return ON_SUBD_RETURN_ERROR(false);

  int quad_fvi0 = 0;
  int quad_dir = 0;
  {
    for (quad_fvi0 = 0; quad_fvi0 < 4; quad_fvi0++)
    {
      const ON_SubDVertex* v = quad_face->Vertex(quad_fvi0);
      if ( nullptr == v )
        return ON_SUBD_RETURN_ERROR(false);
      if (m_vertex_grid[1][1] == v)
      {
        v = quad_face->Vertex((quad_fvi0+1)%4);
        if ( nullptr == v )
          return ON_SUBD_RETURN_ERROR(false);
        if (m_vertex_grid[2][1] == v)
          quad_dir = 1;
        else if (m_vertex_grid[1][2] == v)
          quad_dir = -1;
        else
          return ON_SUBD_RETURN_ERROR(false);
        break;
      }
    }
    if (0 == quad_dir || quad_fvi0 >= 4)
      return ON_SUBD_RETURN_ERROR(false);
  }

  const ON_2dex face_corner_dex[4] = { { 0, 0 }, { 2, 0 }, { 2, 2 }, { 0, 2 } };
  const ON_2dex face_side_dex[4] = { { 1, 0 }, { 2, 1 }, { 1, 2 }, { 0, 1 } };

  const ON_2dex grid_quad_vertex_dex[4] = { { 1,1 }, { 2,1 }, { 2,2 }, { 1,2 } };
  const ON_2dex grid_corner_dex[4] = { { 0, 0 }, { 3, 0 }, { 3, 3 }, { 0, 3 } };
  const ON_2dex grid_side_dex[4][2] = { {{ 1, 0 }, { 2, 0 }}, {{ 3, 1 }, { 3, 2 }}, {{ 2, 3 }, { 1, 3 }}, {{ 0, 2 }, { 0, 1 }} };

  ON_2dex dex;

  const int fvi_map[4] = {
    quad_fvi0,
    (quad_fvi0+4+quad_dir)%4,
    (quad_fvi0+4+2*quad_dir)%4,
    (quad_fvi0+4+3*quad_dir)%4};

  const ON_SubDVertex* quad_vertex[4] = {
    quad_face->Vertex(fvi_map[0]), 
    quad_face->Vertex(fvi_map[1]),
    quad_face->Vertex(fvi_map[2]),
    quad_face->Vertex(fvi_map[3]) };

  const ON_SubDEdgePtr quad_eptr[4] = {
    quad_face->m_edge4[fvi_map[0]],
    quad_face->m_edge4[fvi_map[1]], 
    quad_face->m_edge4[fvi_map[2]],
    quad_face->m_edge4[fvi_map[3]] };

  const ON_SubDEdge* quad_edge[4] = {
    quad_eptr[0].Edge(),
    quad_eptr[1].Edge(),
    quad_eptr[2].Edge(),
    quad_eptr[3].Edge() };

  for (unsigned int fi = 0; fi < 4; fi++)
  {
    if (nullptr == quad_edge[fi])
      return ON_SUBD_RETURN_ERROR(false);
    if (nullptr == quad_edge[fi]->m_vertex[0])
      return ON_SUBD_RETURN_ERROR(false);
    if (nullptr == quad_edge[fi]->m_vertex[1])
      return ON_SUBD_RETURN_ERROR(false);
    if (quad_edge[fi]->m_face_count < 1)
      return ON_SUBD_RETURN_ERROR(false);
    if (nullptr == quad_vertex[fi])
      return ON_SUBD_RETURN_ERROR(false);
    if (quad_vertex[fi]->m_edge_count < 2 || nullptr == quad_vertex[fi]->m_edges )
      return ON_SUBD_RETURN_ERROR(false);
    if (quad_vertex[fi]->m_face_count < 1 || nullptr == quad_vertex[fi]->m_faces )
      return ON_SUBD_RETURN_ERROR(false);
    dex = grid_quad_vertex_dex[fi];
    if ( quad_vertex[fi] != m_vertex_grid[dex.i][dex.j])
      return ON_SUBD_RETURN_ERROR(false);
    if ( quad_edge[fi] != m_center_edges[fi] )
      return ON_SUBD_RETURN_ERROR(false);
    if ( quad_vertex[(fi+1)%4] != quad_edge[fi]->m_vertex[1-quad_eptr[fi].EdgeDirection()] )
      return ON_SUBD_RETURN_ERROR(false);
  }
  
  const ON_SubDFace* side_face[4] = {};
  const ON_SubDFace* corner_face[4] = {};

  for (unsigned int fi = 0; fi < 4; fi++)
  {
    dex = grid_quad_vertex_dex[fi];
    if (quad_vertex[fi] != m_vertex_grid[dex.i][dex.j])
      return ON_SUBD_RETURN_ERROR(false);

    dex = face_side_dex[fi];
    side_face[fi] = m_face_grid[dex.i][dex.j];
    if ( quad_face == side_face[fi])
      return ON_SUBD_RETURN_ERROR(false);

    if (m_bBoundaryCrease[fi])
    {
      // A tag of ON_SubD::EdgeTag::X is an error here
      if ( false == quad_edge[fi]->IsCrease() )
        return ON_SUBD_RETURN_ERROR(false);

      if ( ON_UNSET_UINT_INDEX == quad_edge[fi]->FaceArrayIndex(quad_face) )
        return ON_SUBD_RETURN_ERROR(false);

      if (2 == quad_edge[fi]->m_face_count)
      {
        if ( false == quad_edge[fi]->m_vertex[0]->IsCreaseOrCorner())
          return ON_SUBD_RETURN_ERROR(false);
        if ( false == quad_edge[fi]->m_vertex[1]->IsCreaseOrCorner())
          return ON_SUBD_RETURN_ERROR(false);
      }

      if (nullptr != side_face[fi])
        return ON_SUBD_RETURN_ERROR(false);
    }
    else
    {
      if (nullptr == side_face[fi])
        return ON_SUBD_RETURN_ERROR(false);

      // A tag of ON_SubD::EdgeTag::X is permitted here
      if ( 2 != quad_edge[fi]->m_face_count)
        return ON_SUBD_RETURN_ERROR(false);

      if (quad_edge[fi]->IsCrease())
      {
        unsigned int dart_count = 0;
        unsigned int crease_count = 0;
        if ( ON_SubD::VertexTag::Dart == quad_edge[fi]->m_vertex[0]->m_vertex_tag)
          dart_count++;
        else if ( quad_edge[fi]->m_vertex[0]->IsCreaseOrCorner())
          crease_count++;
        else
          return ON_SUBD_RETURN_ERROR(false);

        if ( ON_SubD::VertexTag::Dart == quad_edge[fi]->m_vertex[1]->m_vertex_tag)
          dart_count++;
        else if ( quad_edge[fi]->m_vertex[1]->IsCreaseOrCorner())
          crease_count++;
        else
          return ON_SUBD_RETURN_ERROR(false);

        if ( 0 == dart_count )
          return ON_SUBD_RETURN_ERROR(false);

        if ( 2 != dart_count + crease_count )
          return ON_SUBD_RETURN_ERROR(false);
      }
      else
      {
        if (false == quad_edge[fi]->IsSmooth())
          return ON_SUBD_RETURN_ERROR(false);
      }
      const ON_SubDFace* edge_faces[2] = { ON_SUBD_FACE_POINTER(quad_edge[fi]->m_face2[0].m_ptr), ON_SUBD_FACE_POINTER(quad_edge[fi]->m_face2[1].m_ptr) };
      if (quad_face == edge_faces[0])
      {
        if (side_face[fi] != edge_faces[1])
          return ON_SUBD_RETURN_ERROR(false);
      }
      else if (quad_face == edge_faces[1])
      {
        if (side_face[fi] != edge_faces[0])
          return ON_SUBD_RETURN_ERROR(false);
      }
      else
        return ON_SUBD_RETURN_ERROR(false);

      if (nullptr == m_edge_grid[fi][0] || nullptr == m_edge_grid[fi][1])
        return ON_SUBD_RETURN_ERROR(false);

      unsigned int side_fei[3] = {};
      side_fei[1] = side_face[fi]->EdgeArrayIndex(quad_edge[fi]);
      if ( ON_UNSET_UINT_INDEX == side_fei[1] )
        return ON_SUBD_RETURN_ERROR(false);

      const ON_SubDEdgePtr side_face_eptr = side_face[fi]->EdgePtr(side_fei[1]);
      if ( quad_edge[fi] != side_face_eptr.Edge())
        return ON_SUBD_RETURN_ERROR(false);

      unsigned int k = (side_face_eptr.EdgeDirection() == quad_eptr[fi].EdgeDirection()) ? 2 : 0;
      unsigned int side_face_edge_count = side_face[fi]->m_edge_count;
      side_fei[2-k] = (side_fei[1] + side_face_edge_count - 1) % side_face_edge_count;
      side_fei[k] = (side_fei[1] + 1) % side_face_edge_count;
      if ( m_edge_grid[fi][0] != side_face[fi]->Edge(side_fei[0]))
        return ON_SUBD_RETURN_ERROR(false);
      if ( m_edge_grid[fi][1] != side_face[fi]->Edge(side_fei[2]))
        return ON_SUBD_RETURN_ERROR(false);
    }

    dex = face_corner_dex[fi];
    corner_face[fi] = m_face_grid[dex.i][dex.j];
    if ( quad_face == corner_face[fi])
      return ON_SUBD_RETURN_ERROR(false);

    bool bCornerShouldExist 
      = 4 == quad_vertex[fi]->m_edge_count
      && 4 == quad_vertex[fi]->m_face_count
      && quad_vertex[fi]->IsSmoothOrDart()
      && false == m_bBoundaryCrease[fi]
      && false == m_bBoundaryCrease[(fi + 3) % 4];
    if (bCornerShouldExist)
    {
      for (unsigned int vei = 0; vei < 4; vei++)
      {
        const ON_SubDEdge* e = quad_vertex[fi]->Edge(vei);
        if ( nullptr == e)
          return ON_SUBD_RETURN_ERROR(false);
        if (2 == e->m_face_count)
        {
          if (e->IsSmooth())
            continue;
          if (e->IsCrease() && ON_SubD::VertexTag::Dart == quad_vertex[fi]->m_vertex_tag)
            continue;
        }
        if (false == e->IsCrease())
          return ON_SUBD_RETURN_ERROR(false);
        bCornerShouldExist = false;
        break;
      }
    }

    dex = grid_corner_dex[fi];
    if (bCornerShouldExist)
    {
      if (nullptr == corner_face[fi])
        return ON_SUBD_RETURN_ERROR(false);
      if (side_face[fi] == corner_face[fi])
        return ON_SUBD_RETURN_ERROR(false);
      if (ON_UNSET_UINT_INDEX == corner_face[fi]->VertexIndex(quad_vertex[fi]))
        return ON_SUBD_RETURN_ERROR(false);
      const unsigned int corner_face_vi = corner_face[fi]->VertexIndex(quad_vertex[fi]);
      if ( ON_UNSET_UINT_INDEX == corner_face_vi)
        return ON_SUBD_RETURN_ERROR(false);
      if (4 == corner_face[fi]->m_edge_count)
      {
        if (nullptr == m_vertex_grid[dex.i][dex.j])
          return ON_SUBD_RETURN_ERROR(false);
        if ( corner_face[fi]->Vertex((corner_face_vi+2)%4) != m_vertex_grid[dex.i][dex.j] )
          return ON_SUBD_RETURN_ERROR(false);
      }
      else
      {
        if (nullptr != m_vertex_grid[dex.i][dex.j])
          return ON_SUBD_RETURN_ERROR(false);
      }
    }
    //else 
    //{
    //  if (nullptr != corner_face[fi])
    //    return ON_SUBD_RETURN_ERROR(false);
    //  if (nullptr != m_vertex_grid[dex.i][dex.j])
    //    return ON_SUBD_RETURN_ERROR(false);
    //}

    if (false == m_bBoundaryCrease[fi])
    {
      for (unsigned int j = 0; j < 2; j++)
      {
        const ON_SubDVertex* v = quad_vertex[(fi + j) % 4];
        unsigned int k = (v != m_edge_grid[fi][j]->m_vertex[0]) ? 0 : 1;
        if (v != m_edge_grid[fi][j]->m_vertex[1 - k])
          return ON_SUBD_RETURN_ERROR(false);
        dex = grid_side_dex[fi][j];
        if (m_vertex_grid[dex.i][dex.j] != m_edge_grid[fi][j]->m_vertex[k])
          return ON_SUBD_RETURN_ERROR(false);
      }
    }
  }

  return true;
}


void ON_SubDQuadNeighborhood::Clear(
  ON_SubDQuadNeighborhood* subd_quad_nbd,
  bool bRetainFixedSizeHeap
)
{
  if (nullptr != subd_quad_nbd)
  {
    ON_SubD_FixedSizeHeap* fsh = (bRetainFixedSizeHeap) ? subd_quad_nbd->m_fsh : nullptr;
    subd_quad_nbd->Internal_Destroy(true);
    subd_quad_nbd->m_fsh = fsh;
  }
}

ON_SubDQuadNeighborhood::~ON_SubDQuadNeighborhood()
{
  Internal_Destroy(false);
}

void ON_SubDQuadNeighborhood::Internal_Destroy(bool bReinitialize)
{
  if (nullptr != m_fsh)
  {
    if (bReinitialize)
      m_fsh->Reset();
    m_fsh = nullptr;
  }

  if (bReinitialize)
  {
    m_bIsCubicPatch = false;
    m_initial_subdivision_level = 0;
    m_current_subdivision_level = 0;

    m_extraordinary_corner_vertex_count = 0;
    m_bExtraordinaryCornerVertex[0] = false;
    m_bExtraordinaryCornerVertex[1] = false;
    m_bExtraordinaryCornerVertex[2] = false;
    m_bExtraordinaryCornerVertex[3] = false;

    m_exact_quadrant_patch_count = 0;
    m_bExactQuadrantPatch[0] = false;
    m_bExactQuadrantPatch[1] = false;
    m_bExactQuadrantPatch[2] = false;
    m_bExactQuadrantPatch[3] = false;

    m_boundary_crease_count = 0;
    m_bBoundaryCrease[0] = false;
    m_bBoundaryCrease[1] = false;
    m_bBoundaryCrease[2] = false;
    m_bBoundaryCrease[3] = false;

    m_bCenterEdgeLimitPoint[0] = false;
    m_bCenterEdgeLimitPoint[1] = false;
    m_bCenterEdgeLimitPoint[2] = false;
    m_bCenterEdgeLimitPoint[3] = false;

    m_center_edge_limit_point[0] = ON_SubDSectorLimitPoint::Nan;
    m_center_edge_limit_point[1] = ON_SubDSectorLimitPoint::Nan;
    m_center_edge_limit_point[2] = ON_SubDSectorLimitPoint::Nan;
    m_center_edge_limit_point[3] = ON_SubDSectorLimitPoint::Nan;

    for (unsigned int i = 0; i < 4; i++)
    {
      m_vertex_grid[i][0] = nullptr;
      m_vertex_grid[i][1] = nullptr;
      m_vertex_grid[i][2] = nullptr;
      m_vertex_grid[i][3] = nullptr;

      m_edge_grid[i][0] = nullptr;
      m_edge_grid[i][1] = nullptr;

      if (i < 3)
      {
        m_face_grid[i][0] = nullptr;
        m_face_grid[i][1] = nullptr;
        m_face_grid[i][2] = nullptr;
      }
    }

    double* dst = &m_srf_cv1[0][0][0];
    double* dst1 = dst + sizeof(m_srf_cv1) / sizeof(m_srf_cv1[0][0][0]);
    while (dst < dst1)
      *dst++ = ON_UNSET_VALUE;
  }
}

static bool IsOrdinarySmoothQuadCornerVertex(
  const ON_SubDVertex* corner_vertex
  )
{
  if ( nullptr == corner_vertex)
    return ON_SUBD_RETURN_ERROR(false);

  if ( 4 != corner_vertex->m_face_count)
    return false;

  if ( 4 != corner_vertex->m_edge_count)
    return false;

  if ( false == corner_vertex->IsSmooth() )
    return false;

  for (unsigned vfi = 0; vfi < 4; vfi++)
  {
    const ON_SubDFace* face = corner_vertex->m_faces[vfi];
    if ( nullptr == face )
      return ON_SUBD_RETURN_ERROR(false);
    if ( 4 != face->m_edge_count )
      return false;
  }

  for (unsigned vei = 0; vei < 4; vei++)
  {
    const ON_SubDEdge* e = ON_SUBD_EDGE_POINTER(corner_vertex->m_edges[vei].m_ptr);
    if ( nullptr == e )
      return ON_SUBD_RETURN_ERROR(false);    
    // Test for exact tag here - do not call e->IsSmooth() because this is a rare case where X tags need to be rejected.
    if ( false == e->IsSmoothNotX() )
      return false;
    if ( 2 != e->m_face_count)
      return ON_SUBD_RETURN_ERROR(false);

    const unsigned int outer_vertex_index = (corner_vertex == e->m_vertex[0]) ? 1U : 0U;
    const ON_SubDVertex* outer_vertex = e->m_vertex[outer_vertex_index];
    if ( nullptr == outer_vertex || corner_vertex == outer_vertex )
      return ON_SUBD_RETURN_ERROR(false);
    if ( outer_vertex->IsSmooth() )
      continue;
    const double sector_coefficient = e->m_sector_coefficient[outer_vertex_index];
    if ( !(0.5 == sector_coefficient) )
      return false;
  }
  return true;
}

bool ON_SubDQuadNeighborhood::VertexGridIsExactCubicPatch(
  const ON_2dex min_face_grid_dex,
  const ON_2dex max_face_grid_dex,
  unsigned int boundary_corner_index
  ) const
{
  // Returns value for  m_bIsCubicPatch

  if (m_extraordinary_corner_vertex_count > 0)
    return false;
  if (m_exact_quadrant_patch_count < 4)
    return false;
  if (m_boundary_crease_count > 2)
    return false;

  int fcount_check;

  if (0 == m_boundary_crease_count)
    fcount_check = 9;
  else if (1 == m_boundary_crease_count)
    fcount_check = 6;
  else if (2 == m_boundary_crease_count)
  {
    if ( boundary_corner_index >= 4 )
      return false;
    fcount_check = 4;
  }
  else
  {
    ON_SUBD_ERROR("Bug in this code.");
    return false;
  }

  for (int i = min_face_grid_dex.i; i < max_face_grid_dex.i; i++)
  {
    for (int j = min_face_grid_dex.j; j < max_face_grid_dex.j; j++)
    {
      const ON_SubDFace* f = m_face_grid[i][j];
      if (nullptr == f || 4 != f->m_edge_count)
      {
        ON_SUBD_ERROR("Bug in this code.");
        return false;
      }
      fcount_check--;
    }
  }

  if (0 != fcount_check)
  {
    ON_SUBD_ERROR("Bug in this code.");
    return false;
  }

  // For the m_vertex_grid[][] to be used as an exact cubic bispan,
  // the outer vertices need to be checked.
  const ON_2dex min_vtx_grid_dex = min_face_grid_dex;
  const ON_2dex max_vtx_grid_dex = { max_face_grid_dex.i + 1, max_face_grid_dex.j + 1 };
  ON_2dex min_smooth_vtx_grid_dex = min_vtx_grid_dex;
  ON_2dex max_smooth_vtx_grid_dex = max_vtx_grid_dex;
  ON_2dex dex;
  if (m_boundary_crease_count > 0)
  {
    ON_2dex crease_vtx_dex[8];
    memset(crease_vtx_dex, 0, sizeof(crease_vtx_dex));
    unsigned int crease_vtx_count = 0;
    if (m_bBoundaryCrease[0])
    {
      dex.j = 1;
      for (dex.i = min_vtx_grid_dex.i; dex.i < max_vtx_grid_dex.i && crease_vtx_count < 8; dex.i++)
        crease_vtx_dex[crease_vtx_count++] = dex;
      min_smooth_vtx_grid_dex.j++;
    }
    if (m_bBoundaryCrease[1])
    {
      dex.i = 2;
      for (dex.j = min_vtx_grid_dex.j; dex.j < max_vtx_grid_dex.j && crease_vtx_count < 8; dex.j++)
        crease_vtx_dex[crease_vtx_count++] = dex;
      max_smooth_vtx_grid_dex.i--;
    }
    if (m_bBoundaryCrease[2])
    {
      dex.j = 2;
      for (dex.i = min_vtx_grid_dex.i; dex.i < max_vtx_grid_dex.i && crease_vtx_count < 8; dex.i++)
        crease_vtx_dex[crease_vtx_count++] = dex;
      max_smooth_vtx_grid_dex.j--;
    }
    if (m_bBoundaryCrease[3])
    {
      dex.i = 1;
      for (dex.j = min_vtx_grid_dex.j; dex.j < max_vtx_grid_dex.j && crease_vtx_count < 8; dex.j++)
        crease_vtx_dex[crease_vtx_count++] = dex;
      min_smooth_vtx_grid_dex.i++;
    }

    switch (m_boundary_crease_count)
    {
    case 1:
      if (4 != crease_vtx_count)
      {
        ON_SUBD_ERROR("Invalid input or a bug above.");
        return false;
      }
      break;

    case 2:
      if (6 != crease_vtx_count)
      {
        ON_SUBD_ERROR("Invalid input or a bug above.");
        return false;
      }
      break;

    default:
      ON_SUBD_ERROR("Invalid input or a bug above.");
      return false;
    }

    for (unsigned int i = 0; i < crease_vtx_count; i++)
    {
      dex = crease_vtx_dex[i];
      const ON_SubDVertex* vertex = m_vertex_grid[dex.i][dex.j];
      if (nullptr == vertex || false == vertex->IsCrease())
      {
        return false;
      }
    }
  }

  for (dex.i = min_smooth_vtx_grid_dex.i; dex.i < max_smooth_vtx_grid_dex.i; dex.i++ )
  {
    for (dex.j = min_smooth_vtx_grid_dex.j; dex.j < max_smooth_vtx_grid_dex.j; dex.j++)
    {
      const ON_SubDVertex* vertex = m_vertex_grid[dex.i][dex.j];
      if (IsOrdinarySmoothQuadCornerVertex(vertex))
        continue;
      return false;
    }
  }

  return true;
}

void ON_SubDQuadNeighborhood::SetPatchStatus(
  const unsigned int fvi0
  )
{
  m_bIsCubicPatch = false;
  const unsigned int delta_subdivision_level 
    = (m_current_subdivision_level > m_initial_subdivision_level)
    ? ((unsigned int)(m_current_subdivision_level - m_initial_subdivision_level))
    : 0U;

  ON_2dex min_face_grid_dex = { 0, 0 };
  ON_2dex max_face_grid_dex = { 3, 3 };

  m_boundary_crease_count = 0;
  if (m_bBoundaryCrease[0])
  {
    m_boundary_crease_count++;
    min_face_grid_dex.j++;
  }
  if (m_bBoundaryCrease[1])
  {
    m_boundary_crease_count++;
    max_face_grid_dex.i--;
  }
  if (m_bBoundaryCrease[2])
  {
    m_boundary_crease_count++;
    max_face_grid_dex.j--;
  }
  if (m_bBoundaryCrease[3])
  {
    m_boundary_crease_count++;
    min_face_grid_dex.i++;
  }


  const unsigned int fvi1 = (fvi0+1)%4;
  const unsigned int fvi2 = (fvi0+2)%4;
  const unsigned int fvi3 = (fvi0+3)%4;

  bool bCenterEdgeIsSmooth[4] = {};
  bCenterEdgeIsSmooth[fvi0] = m_center_edges[fvi0]->IsSmoothNotX();
  bCenterEdgeIsSmooth[fvi1] = (0 == delta_subdivision_level) ? m_center_edges[fvi1]->IsSmoothNotX() : true;
  bCenterEdgeIsSmooth[fvi2] = (0 == delta_subdivision_level) ? m_center_edges[fvi2]->IsSmoothNotX() : true;
  bCenterEdgeIsSmooth[fvi3] = m_center_edges[fvi3]->IsSmoothNotX();

  bool bCenterEdgeIsCrease[4] = {};
  bCenterEdgeIsCrease[fvi0] = bCenterEdgeIsSmooth[fvi0] ? false : m_center_edges[fvi0]->IsCrease();
  bCenterEdgeIsCrease[fvi1] = (0 == delta_subdivision_level) ? m_center_edges[fvi1]->IsCrease() : false;
  bCenterEdgeIsCrease[fvi2] = (0 == delta_subdivision_level) ? m_center_edges[fvi2]->IsCrease() : false;
  bCenterEdgeIsCrease[fvi3] = bCenterEdgeIsSmooth[fvi3] ? false : m_center_edges[fvi3]->IsCrease();

  bool bEdgeTagX = false;
  for (unsigned int i = 0; i < 4; i++)
  {
    if (
      nullptr != m_center_edges[i]
      && ON_SubD::EdgeTag::X != m_center_edges[i]->m_edge_tag
      && (bCenterEdgeIsSmooth[i] != bCenterEdgeIsCrease[i])
      )
    {
      continue;
    }
    bEdgeTagX = true;
    break;
  }

  ////////////////////////////////////////////////////////////////////////////
  //
  // Set 
  //  m_bExtraordinaryCornerVertex[], m_extraordinary_corner_vertex_count
  //  m_bExactQuadrantPatch[], and m_exact_quadrant_patch_count
  // 
  unsigned int boundary_crease_corner_index = 86U;
  unsigned int boundary_corner_corner_index = 86U;

  bool bExtraordinaryCornerVertex[4] = {};
  bExtraordinaryCornerVertex[fvi0] = true;
  bExtraordinaryCornerVertex[fvi1] = (0 == delta_subdivision_level || bEdgeTagX);
  bExtraordinaryCornerVertex[fvi2] = bExtraordinaryCornerVertex[fvi1];
  bExtraordinaryCornerVertex[fvi3] = bExtraordinaryCornerVertex[fvi1];

  if (false == bEdgeTagX)
  {
    const ON_SubDVertex* quad_vertex[4] = {
      m_vertex_grid[1][1],
      m_vertex_grid[2][1],
      m_vertex_grid[2][2],
      m_vertex_grid[1][2]
    };

    const bool bQuadVertexIsSmoothOrCrease[4] = 
    {
      quad_vertex[0]->IsSmoothOrCrease(),
      quad_vertex[1]->IsSmoothOrCrease(),
      quad_vertex[2]->IsSmoothOrCrease(),
      quad_vertex[3]->IsSmoothOrCrease()
    };

    for (unsigned int corner_index = 0; corner_index < 4; corner_index++)
    {
      if (false == bExtraordinaryCornerVertex[corner_index])
        continue;

      if (false == bQuadVertexIsSmoothOrCrease[corner_index] && false == quad_vertex[corner_index]->IsCorner())
        continue;
      if (false == bQuadVertexIsSmoothOrCrease[(corner_index+1)%4])
        continue;
      if (false == bQuadVertexIsSmoothOrCrease[(corner_index+3)%4])
        continue;

      if (bCenterEdgeIsSmooth[corner_index] && bCenterEdgeIsSmooth[(corner_index + 3) % 4])
      {
        if (IsOrdinarySmoothQuadCornerVertex(quad_vertex[corner_index]))
          bExtraordinaryCornerVertex[corner_index] = false;
        continue;
      }

      if (bCenterEdgeIsCrease[corner_index] && bCenterEdgeIsSmooth[(corner_index + 3) % 4])
      {
        if (quad_vertex[corner_index]->IsCrease())
        {
          const ON_SubDEdge* e = m_edge_grid[(corner_index + 3) % 4][1];
          if (nullptr != e && e->IsCrease())
          {
            const ON_SubDFace* f = SideFace((corner_index + 3) % 4);
            if (nullptr != f && 4 == f->m_edge_count)
              bExtraordinaryCornerVertex[corner_index] = false;
          }
        }
        continue;
      }

      if (bCenterEdgeIsSmooth[corner_index] && bCenterEdgeIsCrease[(corner_index + 3) % 4])
      {
        if (quad_vertex[corner_index]->IsCrease())
        {
          const ON_SubDEdge* e = m_edge_grid[corner_index][0];
          if (nullptr != e && e->IsCrease())
          {
            const ON_SubDFace* f = SideFace(corner_index);
            if (nullptr != f && 4 == f->m_edge_count)
              bExtraordinaryCornerVertex[corner_index] = false;
          }
        }
        continue;
      }

      if (bCenterEdgeIsCrease[corner_index] && bCenterEdgeIsCrease[(corner_index + 3) % 4])
      {
        if (
          (quad_vertex[corner_index]->IsCrease() || quad_vertex[corner_index]->IsCorner())
          && quad_vertex[(corner_index + 1) % 4]->IsCrease()
          && quad_vertex[(corner_index + 3) % 4]->IsCrease()
          && IsOrdinarySmoothQuadCornerVertex(quad_vertex[(corner_index + 2) % 4])
          )
        {
          const ON_SubDEdge* e1 = m_edge_grid[(corner_index + 1) % 4][0];
          const ON_SubDEdge* e2 = m_edge_grid[(corner_index + 2) % 4][1];
          if (nullptr != e1 && nullptr != e2 && e1->IsCrease() && e2->IsCrease())
          {
            if (delta_subdivision_level > 0)
            {
              if (quad_vertex[corner_index]->IsCrease())
              {
                boundary_crease_corner_index = corner_index;
                bExtraordinaryCornerVertex[corner_index] = false;
              }
              else if ( quad_vertex[corner_index]->IsCorner() )
              {
                boundary_corner_corner_index = corner_index;
              }
            }
          }
        }
        continue;
      }

    }
  }

  m_extraordinary_corner_vertex_count = 0;
  for (unsigned int corner_index = 0; corner_index < 4; corner_index++)
  {
    m_bExtraordinaryCornerVertex[corner_index] = bExtraordinaryCornerVertex[corner_index];
    if (bExtraordinaryCornerVertex[corner_index])
    {
      m_extraordinary_corner_vertex_count++;
    }
  }

  m_exact_quadrant_patch_count = 0;
  for (unsigned int corner_index = 0; corner_index < 4; corner_index++)
  {
    m_bExactQuadrantPatch[corner_index] = false;
    if (m_boundary_crease_count > 2)
      continue;
    if (2 == m_boundary_crease_count)
    {
      if (boundary_crease_corner_index >= 4)
      {
        if ( boundary_corner_corner_index >= 4 || ((boundary_corner_corner_index+2)%4) != corner_index)
          continue;
      }
    }
    if (bExtraordinaryCornerVertex[corner_index])
      continue;
    if (bExtraordinaryCornerVertex[(corner_index + 1) % 4])
      continue;
    if (bExtraordinaryCornerVertex[(corner_index + 3) % 4])
      continue;
    m_bExactQuadrantPatch[corner_index] = true;
    m_exact_quadrant_patch_count++;
  }

  // Set m_bIsCubicPatch
  m_bIsCubicPatch = VertexGridIsExactCubicPatch(
    min_face_grid_dex,
    max_face_grid_dex,
    boundary_crease_corner_index
    );
}


bool ON_SubDQuadNeighborhood::Set(
  const ON_SubDFace* center_quad_face
  )
{
  ON_SubDQuadNeighborhood::Clear(this, false);

  if (nullptr == center_quad_face)
    return true;

  if (4 != center_quad_face->m_edge_count)
    return ON_SUBD_RETURN_ERROR(false);

  const ON_SubDVertex* qf_vertex[4];
  bool bIsDartVertex[4];
  bool bIsCreaseEdge[4];
  for (unsigned int qfei = 0; qfei < 4; qfei++)
  {
    const ON__UINT_PTR eptr = center_quad_face->m_edge4[qfei].m_ptr;
    const ON_SubDEdge* edge = ON_SUBD_EDGE_POINTER(eptr);
    if (nullptr == edge)
      return ON_SUBD_RETURN_ERROR(false);
    if (nullptr == edge->m_vertex[0])
      return ON_SUBD_RETURN_ERROR(false);
    if (nullptr == edge->m_vertex[1])
      return ON_SUBD_RETURN_ERROR(false);

    bIsCreaseEdge[qfei] = edge->IsCrease();

    m_center_edges[qfei] = edge;

    qf_vertex[qfei] = edge->m_vertex[ON_SUBD_EDGE_DIRECTION(eptr)];
    
    bIsDartVertex[qfei] = qf_vertex[qfei]->IsDart();
  }

  for (unsigned int qfei = 0; qfei < 4; qfei++)
  {
    ON__UINT_PTR ev1 = 1-ON_SUBD_EDGE_DIRECTION(center_quad_face->m_edge4[qfei].m_ptr);
    if ( qf_vertex[(qfei+1)%4] != m_center_edges[qfei]->m_vertex[ev1] )
      return ON_SUBD_RETURN_ERROR(false);
  }
  
  const ON_SubDFace* qf_nbr_face[4] = {};
  for (unsigned int qfei = 0; qfei < 4; qfei++)
  {
    if (bIsCreaseEdge[qfei] && false == bIsDartVertex[qfei] && false == bIsDartVertex[(qfei+1)%4])
    {
      m_bBoundaryCrease[qfei] = true;
      m_boundary_crease_count++;
      continue;
    }
    qf_nbr_face[qfei] = m_center_edges[qfei]->NeighborFace(center_quad_face, false);
  }

  ON_SubDSectorIterator sit0, sit1;

  m_face_grid[1][1] = center_quad_face;
  m_face_grid[1][0] = qf_nbr_face[0];
  m_face_grid[2][1] = qf_nbr_face[1];
  m_face_grid[1][2] = qf_nbr_face[2];
  m_face_grid[0][1] = qf_nbr_face[3];

  m_vertex_grid[1][1] = qf_vertex[0];
  m_vertex_grid[2][1] = qf_vertex[1];
  m_vertex_grid[2][2] = qf_vertex[2];
  m_vertex_grid[1][2] = qf_vertex[3];

  const ON_SubDFace* corner_faces[4] = {};
  const ON_SubDVertex* outer_vertex[12] = {};

  for (unsigned int qfei = 0; qfei < 4; qfei++)
  {
    const unsigned int qfei3 = (qfei+3)%4;

    if ( nullptr == qf_nbr_face[qfei] && nullptr == qf_nbr_face[qfei3])
      continue;

    if (nullptr == sit0.Initialize(center_quad_face, 0, qfei))
      return ON_SUBD_RETURN_ERROR(false);

    if (qf_vertex[qfei] != sit0.CenterVertex())
      return ON_SUBD_RETURN_ERROR(false);

    sit1 = sit0;

    const bool b4EdgedCorner = (4 == qf_vertex[qfei]->m_edge_count && qf_vertex[qfei]->m_face_count >= 3);
    const ON_SubDEdge* e[2] = {};
    const ON_SubDVertex* v[2] = {};
    ON__UINT_PTR eptr;

    for (;;)
    {
      if (nullptr != qf_nbr_face[qfei])
      {
        if (qf_nbr_face[qfei] != sit0.PrevFace(ON_SubDSectorIterator::StopAt::Boundary))
          return ON_SUBD_RETURN_ERROR(false);
        eptr = sit0.CurrentEdgePtr(0).m_ptr;
        e[0] = ON_SUBD_EDGE_POINTER(eptr);
        if (nullptr == e[0])
          return ON_SUBD_RETURN_ERROR(false);
        v[0] = e[0]->m_vertex[1 - ON_SUBD_EDGE_DIRECTION(eptr)];
        if (nullptr == v[0])
          return ON_SUBD_RETURN_ERROR(false);
        
        if (b4EdgedCorner)
        {
          ON_SubDSectorIterator::StopAt stop_at
            = bIsDartVertex[qfei]
            ? ON_SubDSectorIterator::StopAt::Boundary
            : ON_SubDSectorIterator::StopAt::AnyCrease
            ;
          corner_faces[qfei] = sit0.PrevFace(stop_at);
          if (nullptr != corner_faces[qfei])
          {
            eptr = sit0.CurrentEdgePtr(0).m_ptr;
            e[1] = ON_SUBD_EDGE_POINTER(eptr);
            if (nullptr == e[1])
              return ON_SUBD_RETURN_ERROR(false);
            v[1] = e[1]->m_vertex[1 - ON_SUBD_EDGE_DIRECTION(eptr)];
            if (nullptr == v[1])
              return ON_SUBD_RETURN_ERROR(false);
            break;
          }
        }
      }

      if (nullptr == e[1] && nullptr != qf_nbr_face[qfei3])
      {
        if (qf_nbr_face[qfei3] != sit1.NextFace(ON_SubDSectorIterator::StopAt::Boundary))
          return ON_SUBD_RETURN_ERROR(false);
        eptr = sit1.CurrentEdgePtr(1).m_ptr;
        e[1] = ON_SUBD_EDGE_POINTER(eptr);
        if (nullptr == e[1])
          return ON_SUBD_RETURN_ERROR(false);
        v[1] = e[1]->m_vertex[1 - ON_SUBD_EDGE_DIRECTION(eptr)];
        if (nullptr == v[1])
          return ON_SUBD_RETURN_ERROR(false);
        if (b4EdgedCorner && nullptr == corner_faces[qfei])
        {
          ON_SubDSectorIterator::StopAt stop_at
            = bIsDartVertex[qfei3]
            ? ON_SubDSectorIterator::StopAt::Boundary
            : ON_SubDSectorIterator::StopAt::AnyCrease
            ;
          corner_faces[qfei] = sit1.NextFace(stop_at);
          if (nullptr != corner_faces[qfei] && nullptr == e[0] )
          {
            eptr = sit1.CurrentEdgePtr(1).m_ptr;
            e[0] = ON_SUBD_EDGE_POINTER(eptr);
            if (nullptr == e[0])
              return ON_SUBD_RETURN_ERROR(false);
            v[0] = e[0]->m_vertex[1 - ON_SUBD_EDGE_DIRECTION(eptr)];
            if (nullptr == v[0])
              return ON_SUBD_RETURN_ERROR(false);
            break;
          }
        }
      }
      break;
    }

    if ( nullptr != corner_faces[qfei] )
      outer_vertex[3 * qfei] = corner_faces[qfei]->QuadOppositeVertex(qf_vertex[qfei]);

    if (nullptr != e[0])
    {
      m_edge_grid[qfei][0] = e[0];
      outer_vertex[3 * qfei + 1] = v[0];
    }

    if (nullptr != e[1])
    {
      m_edge_grid[qfei3][1] = e[1];
      outer_vertex[(3 * qfei + 11) % 12] = v[1];
    }   
  }

  m_face_grid[0][0] = corner_faces[0]; // lower left corner
  m_face_grid[2][0] = corner_faces[1]; // lower right corner
  m_face_grid[2][2] = corner_faces[2]; // upper right corner
  m_face_grid[0][2] = corner_faces[3]; // upper left corner

  m_vertex_grid[0][0] = outer_vertex[0]; // lower left corner
  m_vertex_grid[1][0] = outer_vertex[1];
  m_vertex_grid[2][0] = outer_vertex[2];
  
  m_vertex_grid[3][0] = outer_vertex[3]; // lower right corner
  m_vertex_grid[3][1] = outer_vertex[4];
  m_vertex_grid[3][2] = outer_vertex[5];

  m_vertex_grid[3][3] = outer_vertex[6]; // upper right corner
  m_vertex_grid[2][3] = outer_vertex[7];
  m_vertex_grid[1][3] = outer_vertex[8];
  
  m_vertex_grid[0][3] = outer_vertex[9]; // upper left corner
  m_vertex_grid[0][2] = outer_vertex[10];
  m_vertex_grid[0][1] = outer_vertex[11];

  m_initial_subdivision_level = 0;
  m_current_subdivision_level = 0;
  
  SetPatchStatus(0);
  
#if defined(ON_DEBUG)
  IsValid(); // will trigger a break if "this" is not valid
#endif
  
  return true;
}

const ON_SubDFace* ON_SubDQuadNeighborhood::CenterQuad() const
{
  return m_face_grid[1][1];
}

const ON_SubDVertex* ON_SubDQuadNeighborhood::CenterVertex(
  int vi
  ) const
{
  if (0==vi)
    return m_vertex_grid[1][1];
  if (1==vi)
    return m_vertex_grid[2][1];
  if (2==vi)
    return m_vertex_grid[2][2];
  if (3==vi)
    return m_vertex_grid[1][2];
  return ON_SUBD_RETURN_ERROR(nullptr);
}

const ON_2dex ON_SubDQuadNeighborhood::CenterVertexDex(
  int vi
)
{
  if (0 == vi)
    return ON_2dex(1, 1);
  if (1==vi)
    return ON_2dex(2, 1);
  if (2==vi)
    return ON_2dex(2, 2);
  if (3==vi)
    return ON_2dex(1, 2);
  return ON_2dex(ON_UNSET_INT_INDEX,ON_UNSET_INT_INDEX);
}


const ON_SubDFace* ON_SubDQuadNeighborhood::SideFace(
  unsigned int fei
  ) const
{
  ON_2dex dex = ON_SubDQuadNeighborhood::GridDex(3,fei,1,0);
  return m_face_grid[dex.i][dex.j];
}

const ON_SubDFace* ON_SubDQuadNeighborhood::CornerFace(
  unsigned int fvi
  ) const
{
  ON_2dex dex = ON_SubDQuadNeighborhood::GridDex(3,fvi,0,0);
  return m_face_grid[dex.i][dex.j];
}



bool ON_SubDQuadNeighborhood::GetLimitSurfaceCV(
  //double srf_cv[4][4][3]
  double* srf_cv,
  unsigned int srf_cv_grid_size // 4 or 5
  ) const
{
  if (nullptr == m_face_grid[1][1] || false == m_bIsCubicPatch)
    return ON_SUBD_RETURN_ERROR(false);

  const double* srcP;
  double *dstP;

  // Get the central quad face corners
  int Pcount = 0;
  int i0, i1, j0, j1;
  if (m_boundary_crease_count > 0)
  {
    if (m_boundary_crease_count >1)
      return ON_SUBD_RETURN_ERROR(false);

    if (m_bBoundaryCrease[0])
    {
      j0 = j1 = 0;
      i0 = 0;
      i1 = 3;
    }
    else if (m_bBoundaryCrease[1])
    {
      i0 = i1 = 3;
      j0 = 0;
      j1 = 3;
    }
    else if (m_bBoundaryCrease[2])
    {
      j0 = j1 = 3;
      i0 = 0;
      i1 = 3;
    }
    else if (m_bBoundaryCrease[3])
    {
      i0 = i1 = 0;
      j0 = 0;
      j1 = 3;
    }
    else
      return ON_SUBD_RETURN_ERROR(false);
  }
  else
  {
    i0 = -1;
    i1 = -1;
    j0 = -1;
    j1 = -1;
  }

  for (int i = 0; i < 4; i++)
  {
    for (int j = 0; j < 4; j++)
    {
      if (i >= i0 && i <= i1 && j >= j0 && j <= j1)
        continue;
      if (nullptr == m_vertex_grid[i][j])
        return ON_SUBD_RETURN_ERROR(false);
      //dstP = srf_cv[i][j];
      dstP = srf_cv + 3*(i*srf_cv_grid_size+j);
      srcP = m_vertex_grid[i][j]->m_P;
      *dstP++ = *srcP++; *dstP++ = *srcP++; *dstP = *srcP;
      Pcount++;
    }
  }

  if ( 16 == Pcount)
    return true;

  if (12 == Pcount)
  {
    // crease case
    const int di = (i0 == i1) ? (0 == i0 ? 1 : -1) : 0;
    const int dj = (j0 == j1) ? (0 == j0 ? 1 : -1) : 0;
    i1++;
    j1++;
    for (int i = i0; i < i1; i++)
    {
      for (int j = j0; j < j1; j++)
      {
        const ON_SubDVertex* v[2] = { m_vertex_grid[i + di][j + dj], m_vertex_grid[i + 2 * di][j + 2 * dj] };
        if (nullptr == v[0] || nullptr == v[1])
          return ON_SUBD_RETURN_ERROR(false);
        if (ON_SubD::VertexTag::Crease != v[0]->m_vertex_tag)
          return ON_SUBD_RETURN_ERROR(false);
        //dstP = srf_cv[i][j];
        dstP = srf_cv + 3*(i*srf_cv_grid_size+j);
        dstP[0] = 2.0 * v[0]->m_P[0] - v[1]->m_P[0];
        dstP[1] = 2.0 * v[0]->m_P[1] - v[1]->m_P[1];
        dstP[2] = 2.0 * v[0]->m_P[2] - v[1]->m_P[2];
      }
    }
    return true;
  }


  return ON_SUBD_RETURN_ERROR(false);
}

bool ON_SubDQuadNeighborhood::GetSubdivisionPoint(
  const ON_SubDVertex* vertex,
  double subdivision_point[3]
  )
{
  if (nullptr == subdivision_point)
    return ON_SUBD_RETURN_ERROR(false);
  for (;;)
  {
    if (nullptr==vertex)
      break;
    double Q[3];
    if (!vertex->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark,true,Q))
      break;
    subdivision_point[0] = Q[0];
    subdivision_point[1] = Q[1];
    subdivision_point[2] = Q[2];
  }
  subdivision_point[0] = ON_UNSET_VALUE;
  subdivision_point[1] = ON_UNSET_VALUE;
  subdivision_point[2] = ON_UNSET_VALUE;
  return ON_SUBD_RETURN_ERROR(false);
}

bool ON_SubDQuadNeighborhood::GetSubdivisionPoint(
  const ON_SubDEdge* edge,
  double subdivision_point[3]
  )
{
  if (nullptr == subdivision_point)
    return ON_SUBD_RETURN_ERROR(false);
  for (;;)
  {
    if (nullptr==edge)
      break;
    double Q[3];
    if (!edge->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark,true,Q))
      break;
    subdivision_point[0] = Q[0];
    subdivision_point[1] = Q[1];
    subdivision_point[2] = Q[2];
  }
  subdivision_point[0] = ON_UNSET_VALUE;
  subdivision_point[1] = ON_UNSET_VALUE;
  subdivision_point[2] = ON_UNSET_VALUE;
  return ON_SUBD_RETURN_ERROR(false);
}


bool ON_SubDQuadNeighborhood::GetSubdivisionPoint(
  const ON_SubDFace* face,
  double subdivision_point[3]
  )
{
  if (nullptr == subdivision_point)
    return ON_SUBD_RETURN_ERROR(false);
  for (;;)
  {
    if (nullptr==face)
      break;
    double Q[3];
    if (!face->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark,true,Q))
      break;
    subdivision_point[0] = Q[0];
    subdivision_point[1] = Q[1];
    subdivision_point[2] = Q[2];
  }
  subdivision_point[0] = ON_UNSET_VALUE;
  subdivision_point[1] = ON_UNSET_VALUE;
  subdivision_point[2] = ON_UNSET_VALUE;
  return ON_SUBD_RETURN_ERROR(false);
}

unsigned int ON_SubDQuadNeighborhood::SetLimitSubSurfaceExactCVs(
  unsigned int quadrant_index
  )
{
  if (nullptr == m_face_grid[1][1] || quadrant_index > 4)
    return ON_SUBD_RETURN_ERROR(0);

  const bool bUseSavedSubdivisionPoint = true;

  ON_2dex dex;
  ON_2dex deltadex;
  const ON_SubDFace* face;
  unsigned int i;
  double Q[3][3];
  double* P1;

  if (!ON_IsValid(m_srf_cv1[2][2][0]))
  {
    // all sub surfaces require inner 3x3 grid of subdivision points
    face = m_face_grid[1][1];
    if (4 != face->m_edge_count)
      return ON_SUBD_RETURN_ERROR(0);

    // The value of m_srf_cv1[2][2][0] is used to determine when the inner 3x3 grid is set, 
    // so its value must be set after the 8 cvs around it are successfully set.
    // The value 
    //   Q[2] = face subd point 
    // is calculated here because if face->GetSubdivisionPoint() fails,
    // nothing below should succeed. The value of Q[2] is assigned to m_srf_cv1[2][2]
    // after the 8 ring points are successfully calculated.
    if (!face->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark, bUseSavedSubdivisionPoint, Q[2]))
      return ON_SUBD_RETURN_ERROR(0);

    // faces_vertices[] face, in counterclockwise order.  
    // m_center_edges[] are the 4 edges of face in counterclockwise order with 
    // m_center_edges[0] connecting face_vertices[0] and face_vertices[1].
    // However, it may be that face->Vertex(0) != face_vertices[0].
    const ON_SubDVertex* faces_vertices[4] = { m_vertex_grid[1][1], m_vertex_grid[2][1], m_vertex_grid[2][2], m_vertex_grid[1][2] };

    const ON_2dex srf_cv_dex[8] = { { 1, 1 }, { 2, 1 }, { 3, 1 }, { 3, 2 }, { 3, 3 }, { 2, 3 }, { 1, 3 }, { 1, 2 } };

    for (unsigned int fei = 0; fei < 4; fei++)
    {
      if (nullptr == faces_vertices[fei])
        return ON_SUBD_RETURN_ERROR(0);
      if (!faces_vertices[fei]->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark, bUseSavedSubdivisionPoint, Q[0]))
        return ON_SUBD_RETURN_ERROR(0);
      if (nullptr == m_center_edges[fei])
        return ON_SUBD_RETURN_ERROR(0);
      if (!m_center_edges[fei]->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark, bUseSavedSubdivisionPoint, Q[1]))
        return ON_SUBD_RETURN_ERROR(0);

      dex = srf_cv_dex[2 * fei];
      P1 = m_srf_cv1[dex.i][dex.j];
      P1[0] = Q[0][0]; P1[1] = Q[0][1]; P1[2] = Q[0][2];

      dex = srf_cv_dex[2 * fei + 1];
      P1 = m_srf_cv1[dex.i][dex.j];
      P1[0] = Q[1][0]; P1[1] = Q[1][1]; P1[2] = Q[1][2];
    }

    // m_srf_cv1[2][2][0] is used to determine when the inner 3x3 grid is set, 
    // so its value must be set after the 8 cvs around it are successfully set.
    P1 = m_srf_cv1[2][2];
    P1[0] = Q[2][0]; P1[1] = Q[2][1]; P1[2] = Q[2][2];
  }

  const unsigned int fvi_min = (4 == quadrant_index) ? 0 : quadrant_index;
  const unsigned int fvi_max = (4 == quadrant_index) ? 4 : fvi_min+1;
  unsigned int quadrant_count = 0;
  for (unsigned int fvi = fvi_min; fvi < fvi_max; fvi++)
  {
    if (false == m_bExactQuadrantPatch[fvi])
      continue;
    quadrant_count++;
    const unsigned int fvi3 = (fvi + 3) % 4;
    for (unsigned int side_pass = 0; side_pass < 2; side_pass++)
    {
      const unsigned int side_fvi = (0 == side_pass) ? fvi : fvi3;

      dex = ON_SubDQuadNeighborhood::GridDex(5, side_fvi, 1, 0);
      deltadex = ON_SubDQuadNeighborhood::DeltaDex(side_fvi, 1, 0);

      P1 = &m_srf_cv1[dex.i][dex.j][0];
      if ( !ON_IsValid(P1[0]) )
      {
        bool bEvaluateCrease = m_bBoundaryCrease[side_fvi] || m_center_edges[side_fvi]->IsCrease();
        if (bEvaluateCrease)
        {
          ON_2dex Adex = ON_SubDQuadNeighborhood::GridDex(5, side_fvi, 1, 1);
          ON_2dex Bdex = ON_SubDQuadNeighborhood::GridDex(5, side_fvi, 1, 2);
          for (i = 0; i < 3; i++)
          {
            const double* A = m_srf_cv1[Adex.i][Adex.j];
            const double* B = m_srf_cv1[Bdex.i][Bdex.j];
            Q[i][0] = 2.0*A[0] - B[0];
            Q[i][1] = 2.0*A[1] - B[1];
            Q[i][2] = 2.0*A[2] - B[2];
            Adex.i += deltadex.i;
            Adex.j += deltadex.j;
            Bdex.i += deltadex.i;
            Bdex.j += deltadex.j;
          }
        }
        else if ( m_center_edges[side_fvi]->IsSmoothNotX() )
        {
          const ON_SubDEdge* edge = m_edge_grid[side_fvi][0];
          if (nullptr == edge)
            return ON_SUBD_RETURN_ERROR(0);
          if (!edge->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark, bUseSavedSubdivisionPoint, Q[0]))
            return ON_SUBD_RETURN_ERROR(0);

          const ON_2dex fdex = ON_SubDQuadNeighborhood::GridDex(3, side_fvi, 1, 0);
          face = m_face_grid[fdex.i][fdex.j];
          if (nullptr == face)
            return ON_SUBD_RETURN_ERROR(0);
          if (!face->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark, bUseSavedSubdivisionPoint, Q[1]))
            return ON_SUBD_RETURN_ERROR(0);

          edge = m_edge_grid[side_fvi][1];
          if (nullptr == edge)
            return ON_SUBD_RETURN_ERROR(0);
          if (!edge->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark, bUseSavedSubdivisionPoint, Q[2]))
            return ON_SUBD_RETURN_ERROR(0);
        }

        for (i = 0; i < 3; i++)
        {
          P1 = m_srf_cv1[dex.i][dex.j];
          P1[0] = Q[i][0]; P1[1] = Q[i][1]; P1[2] = Q[i][2];
          dex.i += deltadex.i;
          dex.j += deltadex.j;
        }
      }
    }

    dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 0, 0);
    P1 = &m_srf_cv1[dex.i][dex.j][0];
    if (!ON_IsValid(P1[0]))
    {
      if (m_bBoundaryCrease[fvi] && m_bBoundaryCrease[fvi3])
      {
        dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 2, 1);
        Q[0][0] = m_srf_cv1[dex.i][dex.j][0];
        Q[0][1] = m_srf_cv1[dex.i][dex.j][1];
        Q[0][2] = m_srf_cv1[dex.i][dex.j][2];
        dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 1, 2);
        Q[1][0] = m_srf_cv1[dex.i][dex.j][0];
        Q[1][1] = m_srf_cv1[dex.i][dex.j][1];
        Q[1][2] = m_srf_cv1[dex.i][dex.j][2];
        dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 2, 2);
        Q[2][0] = m_srf_cv1[dex.i][dex.j][0];
        Q[2][1] = m_srf_cv1[dex.i][dex.j][1];
        Q[2][2] = m_srf_cv1[dex.i][dex.j][2];

        dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 1, 1);
        //const double c = 4.0;
        //const double b = -2.0;
        const double c = -8.0;
        const double b = 4.0;
        P1[0] = c*m_srf_cv1[dex.i][dex.j][0] + b*(Q[0][0] + Q[1][0]) + Q[2][0];
        P1[1] = c*m_srf_cv1[dex.i][dex.j][1] + b*(Q[0][1] + Q[1][1]) + Q[2][1];
        P1[2] = c*m_srf_cv1[dex.i][dex.j][2] + b*(Q[0][2] + Q[1][2]) + Q[2][2];
      }
      else if (m_bBoundaryCrease[fvi])
      {
        dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 0, 1);
        Q[0][0] = m_srf_cv1[dex.i][dex.j][0];
        Q[0][1] = m_srf_cv1[dex.i][dex.j][1];
        Q[0][2] = m_srf_cv1[dex.i][dex.j][2];
        dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 0, 2);
        Q[1][0] = m_srf_cv1[dex.i][dex.j][0];
        Q[1][1] = m_srf_cv1[dex.i][dex.j][1];
        Q[1][2] = m_srf_cv1[dex.i][dex.j][2];

        P1[0] = 2.0*Q[0][0] - Q[1][0];
        P1[1] = 2.0*Q[0][1] - Q[1][1];
        P1[2] = 2.0*Q[0][2] - Q[1][2];
      }
      else if (m_bBoundaryCrease[fvi3])
      {
        dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 1, 0);
        Q[0][0] = m_srf_cv1[dex.i][dex.j][0];
        Q[0][1] = m_srf_cv1[dex.i][dex.j][1];
        Q[0][2] = m_srf_cv1[dex.i][dex.j][2];
        dex = ON_SubDQuadNeighborhood::GridDex(5, fvi, 2, 0);
        Q[1][0] = m_srf_cv1[dex.i][dex.j][0];
        Q[1][1] = m_srf_cv1[dex.i][dex.j][1];
        Q[1][2] = m_srf_cv1[dex.i][dex.j][2];

        P1[0] = 2.0*Q[0][0] - Q[1][0];
        P1[1] = 2.0*Q[0][1] - Q[1][1];
        P1[2] = 2.0*Q[0][2] - Q[1][2];
      }
      else
      {
        dex = ON_SubDQuadNeighborhood::GridDex(3, fvi, 0, 0);
        const ON_SubDFace* face_ij = m_face_grid[dex.i][dex.j];
        if (nullptr == face_ij)
          return ON_SUBD_RETURN_ERROR(0);
        if (!face_ij->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark, bUseSavedSubdivisionPoint, Q[0]))
          return ON_SUBD_RETURN_ERROR(0);
        P1[0] = Q[0][0]; P1[1] = Q[0][1]; P1[2] = Q[0][2];
      }
    }
  }

  return quadrant_count;
}

bool ON_SubDQuadNeighborhood::GetLimitSubSurfaceSinglePatchCV(
  unsigned int fvi,
  double srf_cv[4][4][3]
  )
{
  if (fvi >= 4)
    return ON_SUBD_RETURN_ERROR(false);

  if (false == m_bExactQuadrantPatch[fvi])
    return ON_SUBD_RETURN_ERROR(false);

  unsigned int quadrant_count = SetLimitSubSurfaceExactCVs(fvi);
  if ( 1 != quadrant_count )
    return ON_SUBD_RETURN_ERROR(false);

  ON_2dex dex;

  dex.i = 0;
  dex.j = 0;
  if (1 == fvi || 2 == fvi)
    dex.i++;
  if (2 == fvi || 3 == fvi)
    dex.j++;

  double* P1 = srf_cv[0][0];
  for (unsigned int i = 0; i < 4; i++)
  {
    for (unsigned int j = 0; j < 4; j++)
    {
      //double* P1 = srf_cv[i][j];
      const double* src = m_srf_cv1[i+dex.i][j+dex.j];
      *P1++ = *src++;
      *P1++ = *src++;
      *P1++ = *src;
    }
  }

  return true;
}


unsigned int ON_SubDQuadNeighborhood::ExtraordinaryCenterVertexIndex(
  ON_SubD::VertexTag vertex_tag_filter,
  unsigned int minimum_edge_count_filter
) const
{
  for(;;)
  {
    if (1 != m_extraordinary_corner_vertex_count)
      break;
    if (1 != m_exact_quadrant_patch_count)
      break;
    const unsigned int extraordinary_vertex_index
      = m_bExtraordinaryCornerVertex[0] ? 0
      : (m_bExtraordinaryCornerVertex[1] ? 1
        : (m_bExtraordinaryCornerVertex[2] ? 2 : 3));
      if (false == (m_bExtraordinaryCornerVertex[extraordinary_vertex_index]))
        break;
      if (false == (m_bExactQuadrantPatch[(extraordinary_vertex_index + 2) % 4]))
        break;
      const ON_2dex dex = CenterVertexDex(extraordinary_vertex_index);
      if (dex.i < 1 || dex.i > 2 || dex.j < 1 || dex.j > 2)
        break;
      if (nullptr == m_vertex_grid[dex.i][dex.j])
        break;
      if (ON_SubD::VertexTag::Corner != m_vertex_grid[dex.i][dex.j]->m_vertex_tag)
      {
        if (((unsigned int)(m_vertex_grid[dex.i][dex.j]->m_edge_count)) < minimum_edge_count_filter)
          break;
        if (
          ON_SubD::VertexTag::Unset != vertex_tag_filter
          && m_vertex_grid[dex.i][dex.j]->m_vertex_tag != vertex_tag_filter
          )
        {
          break;
        }
      }
      return extraordinary_vertex_index;
  }
  return ON_UNSET_UINT_INDEX;
}


bool ON_SubDQuadNeighborhood::Internal_GetApproximateCV(
  int i,
  int j,
  double unset_cv,
  double approximate_cv[3]
  ) const
{
  approximate_cv[0] = unset_cv;
  approximate_cv[1] = unset_cv;
  approximate_cv[2] = unset_cv;

  const ON_SubDEdge* e = nullptr;
  const ON_SubDFace* f = nullptr;
  if (0 == j)
  {
    switch (i)
    {
    case 0:
      if ( false == m_bExtraordinaryCornerVertex[0] )
        f = m_face_grid[0][0];
      break;
    case 1:
      e = m_edge_grid[0][0];
      break;
    case 2:
      f = m_face_grid[1][0];
      break;
    case 3:
      e = m_edge_grid[0][1];
      break;
    case 4:
      if ( false == m_bExtraordinaryCornerVertex[1] )
        f = m_face_grid[2][0];
      break;
    }
  }
  else if (4 == i)
  {
    switch (j)
    {
    // case 0:  // i = 0; j = 0 handled above
    case 1:
      e = m_edge_grid[1][0];
      break;
    case 2:
      f = m_face_grid[2][1];
      break;
    case 3:
      e = m_edge_grid[1][1];
      break;
    case 4:
      if ( false == m_bExtraordinaryCornerVertex[2] )
        f = m_face_grid[2][2];
      break;
    }
  }
  else if (4 == j)
  {
    switch (i)
    {
    case 0:
      if ( false == m_bExtraordinaryCornerVertex[3] )
        f = m_face_grid[0][2];
      break;
    case 1:
      e = m_edge_grid[2][1];
      break;
    case 2:
      f = m_face_grid[1][2];
      break;
    case 3:
      e = m_edge_grid[2][0];
      break;
    // case 4:  // i = 4; j = 4 handled above
    }
  }
  else if (0 == i)
  {
    switch (j)
    {
    // case 0:  // i = 0; j = 0 handled above
    case 1:
      e = m_edge_grid[3][1];
      break;
    case 2:
      f = m_face_grid[0][1];
      break;
    case 3:
      e = m_edge_grid[3][0];
      break;
    // case 4:  // i = 0; j = 4 handled above
    }
  }
  
  bool bHaveApproximateCV;
  const bool bUseSavedSubdivisionPoint = true;
  if (nullptr != e)
  {
    const int extraordinary_vertex_index = ExtraordinaryCenterVertexIndex(ON_SubD::VertexTag::Crease, 4);
    const ON_SubDVertex* extraordinary_vertex
      = (extraordinary_vertex_index >= 0 && extraordinary_vertex_index < 4)
      ? CenterVertex(extraordinary_vertex_index)
      : nullptr;
    if (
      (ON_SubD::EdgeTag::Smooth == e->m_edge_tag || ON_SubD::EdgeTag::Crease == e->m_edge_tag)
      && (e->m_vertex[0] == extraordinary_vertex || e->m_vertex[1] == extraordinary_vertex)
      )
    {
      // extraordinary crease vertices
      bHaveApproximateCV = false;
    }
    else
    {
      bHaveApproximateCV = e->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark, bUseSavedSubdivisionPoint, approximate_cv);
    }
  }
  else if ( nullptr != f && 4 == f->m_edge_count )
    bHaveApproximateCV = f->GetSubdivisionPoint(ON_SubD::SubDType::QuadCatmullClark,bUseSavedSubdivisionPoint,approximate_cv);
  else
  {
    bHaveApproximateCV = false;
  }

  return bHaveApproximateCV;
}



static double ON_SubDQuadFaceTopology_CopySectorWeight(
  const ON_SubDEdge* e0,
  const ON_SubDVertex* e0v
  )
{
  if (nullptr == e0 || nullptr == e0v)
    return ON_SUBD_RETURN_ERROR(false);

  if (ON_SubD::EdgeTag::Smooth != e0->m_edge_tag && ON_SubD::EdgeTag::X != e0->m_edge_tag )
    return ON_SubDSectorType::IgnoredSectorWeight;

  if (e0v == e0->m_vertex[0])
    return e0->m_sector_coefficient[0];
  
  if (e0v == e0->m_vertex[1])
    return e0->m_sector_coefficient[1];

  return ON_SUBD_RETURN_ERROR(ON_UNSET_VALUE);
}

static ON_SubDEdge* ON_SubDQuadFaceTopology_SubdivideEdge(
  ON_SubD_FixedSizeHeap& fsh,
  ON_SubDVertex* qv1,
  const ON_SubDVertex* qv0,
  const ON_SubDEdge* e0
  )
{
  if (nullptr == qv1 || nullptr == e0)
    return ON_SUBD_RETURN_ERROR(nullptr);

  ON_SubDVertex* v1 = fsh.AllocateVertex(e0,ON_SubD::SubDType::QuadCatmullClark,true,4,4);
  if (nullptr == v1)
    return ON_SUBD_RETURN_ERROR(nullptr);

  double v0_weight;
  if ( e0->IsSmooth() && nullptr != qv0)
  {
    // qv1 is the subdivision point of qv0.
    if ( qv1->m_vertex_tag != qv0->m_vertex_tag )
      return ON_SUBD_RETURN_ERROR(nullptr);
    if ( ON_SubD::VertexTag::Smooth == qv0->m_vertex_tag)
      v0_weight = ON_SubDSectorType::IgnoredSectorWeight;
    else
    {
      v0_weight = ON_SubDQuadFaceTopology_CopySectorWeight(e0, qv0);
      if (false == ON_SubDSectorType::IsValidSectorWeightValue(v0_weight,false))
        return ON_SUBD_RETURN_ERROR(nullptr);
    }
  }
  else
    v0_weight = ON_SubDSectorType::IgnoredSectorWeight;

  const double v1_weight = ON_SubDSectorType::IgnoredSectorWeight;

  ON_SubDEdge* e1 = fsh.AllocateEdge(qv1,v0_weight,v1,v1_weight);
  if (nullptr == e1)
    return ON_SUBD_RETURN_ERROR(nullptr);
  if (e1->m_edge_tag != e0->m_edge_tag)
  {
    // On the first subdivision step,
    // e0 with tag ON_SubD::EdgeTag::X turns into 
    // e1 with tag ON_SubD::EdgeTag::Smooth.
    if ( ON_SubD::EdgeTag::Smooth != e1->m_edge_tag || ON_SubD::EdgeTag::X != e0->m_edge_tag)
      return ON_SUBD_RETURN_ERROR(nullptr);
  }

  return e1;
}

static ON_SubDFace* ON_SubDQuadFaceTopology_SubdivideFace(
  ON_SubD_FixedSizeHeap& fsh,
  const ON_SubDFace* f0,
  ON_SubDEdge* e1[2],
  double at_crease_weight
  )
{
  ON_SubDVertex* v[4];
  if (nullptr == f0 || nullptr == e1[0] || nullptr == e1[1])
    return ON_SUBD_RETURN_ERROR(nullptr);

  v[0] = const_cast<ON_SubDVertex*>(e1[0]->m_vertex[0]);
  if (nullptr == v[0] || v[0] != e1[1]->m_vertex[0])
    return ON_SUBD_RETURN_ERROR(nullptr);

  v[1] = const_cast<ON_SubDVertex*>(e1[0]->m_vertex[1]);
  if (nullptr == v[1] )
    return ON_SUBD_RETURN_ERROR(nullptr);

  v[3] = const_cast<ON_SubDVertex*>(e1[1]->m_vertex[1]);
  if (nullptr == v[3] )
    return ON_SUBD_RETURN_ERROR(nullptr);

  if (v[1] == v[0] || v[3] == v[0] || v[1] == v[3])
    return ON_SUBD_RETURN_ERROR(nullptr);

  v[2] = fsh.AllocateVertex(f0,ON_SubD::SubDType::QuadCatmullClark,true,4,4);
  if ( nullptr == v[2])
    return ON_SUBD_RETURN_ERROR(nullptr);

  const double v1_weight = (ON_SubD::VertexTag::Crease == v[1]->m_vertex_tag) ? at_crease_weight : ON_SubDSectorType::IgnoredSectorWeight;
  const double v2_weight = ON_SubDSectorType::IgnoredSectorWeight;
  const double v3_weight = (ON_SubD::VertexTag::Crease == v[3]->m_vertex_tag) ? at_crease_weight : ON_SubDSectorType::IgnoredSectorWeight;

  ON_SubDEdge* e12 = fsh.AllocateEdge(v[1],v1_weight,v[2],v2_weight);
  if ( nullptr == e12)
    return ON_SUBD_RETURN_ERROR(nullptr);

  ON_SubDEdge* e23 = fsh.AllocateEdge(v[2],v2_weight,v[3],v3_weight);
  if ( nullptr == e23)
    return ON_SUBD_RETURN_ERROR(nullptr);

  ON_SubDEdgePtr f1_epts[4] = {
    ON_SubDEdgePtr::Create(e1[0], 0),
    ON_SubDEdgePtr::Create(e12, 0),
    ON_SubDEdgePtr::Create(e23, 0),
    ON_SubDEdgePtr::Create(e1[1], 1)
  };

  ON_SubDFace* f1 = fsh.AllocateQuad(f0->m_zero_face_id, f0->m_id, f1_epts);
  if ( nullptr == f1)
    return ON_SUBD_RETURN_ERROR(nullptr);

  return f1;
}

bool ON_SubDQuadNeighborhood::Subdivide(
  const unsigned int q0fvi,
  ON_SubD_FixedSizeHeap& fsh,
  class ON_SubDQuadNeighborhood* q1ft
  ) const
{
  if ( nullptr == q1ft || this == q1ft)
    return ON_SUBD_RETURN_ERROR(false);

  if ( m_fsh == &fsh )
    return ON_SUBD_RETURN_ERROR(false);

  const ON_SubD::SubDType subd_type = ON_SubD::SubDType::QuadCatmullClark;

  // When a smooth subdivision edge ends at a vertex that is a subdivision point
  // of a creased original edge, this is the value to assign to the new
  // edge's m_vertex_weight. The "2" is there because there would be 2
  // sector faces if the subdivision was complete.
  const double at_crease_weight = ON_SubDSectorType::CreaseSectorWeight(subd_type,2);
  
  if ( m_fsh == q1ft->m_fsh)
    q1ft->m_fsh = nullptr;
  ON_SubDQuadNeighborhood::Clear(q1ft, false);
  q1ft->m_fsh = nullptr;

  q1ft->m_initial_subdivision_level = m_initial_subdivision_level;
  q1ft->m_current_subdivision_level = m_current_subdivision_level + 1;

  if (q0fvi > 3)
    return ON_SUBD_RETURN_ERROR(false);

  const ON_SubDFace* qf0 = CenterQuad();
  if ( nullptr == qf0 || 4 != qf0->m_edge_count)
    return ON_SUBD_RETURN_ERROR(false);

  const unsigned int zero_face_id = qf0->m_zero_face_id;
  const unsigned int parent_face_id = qf0->m_id;

  const ON_SubDEdge* qf0_edges[4] = {
    m_center_edges[q0fvi],
    m_center_edges[(q0fvi+1)%4],
    m_center_edges[(q0fvi+2)%4],
    m_center_edges[(q0fvi+3)%4]};

  if (nullptr == qf0_edges[0] || nullptr == qf0_edges[1] || nullptr == qf0_edges[2] || nullptr == qf0_edges[3])
    return ON_SUBD_RETURN_ERROR(false);

  const ON_SubDVertex* qf0_vertices[4] = {
    CenterVertex(q0fvi),
    CenterVertex((q0fvi+1)%4),
    CenterVertex((q0fvi+2)%4),
    CenterVertex((q0fvi+3)%4)};
  if (nullptr == qf0_vertices[0] || nullptr == qf0_vertices[1] || nullptr == qf0_vertices[2] || nullptr == qf0_vertices[3])
    return ON_SUBD_RETURN_ERROR(false);

  const ON_SubDVertex* qv0 = qf0_vertices[0];
  if ( nullptr == qv0 || qv0->m_face_count > qv0->m_edge_count)
    return ON_SUBD_RETURN_ERROR(false);

  const unsigned int N = qv0->m_edge_count;
  if (N < ON_SubDSectorType::MinimumSectorEdgeCount(qv0->m_vertex_tag))
    return ON_SUBD_RETURN_ERROR(false);

  ON_SubDSectorIterator sit;
  if ( nullptr == sit.Initialize(qf0,0,qv0) )
    return ON_SUBD_RETURN_ERROR(false);

  const bool bIsDartSector = (ON_SubD::VertexTag::Dart == qv0->m_vertex_tag);
  const bool bIsCreaseOrCornerSector = qv0->IsCreaseOrCorner();

  const bool bBoundaryCrease1[4] = {
    m_bBoundaryCrease[q0fvi] || (bIsCreaseOrCornerSector && qf0_edges[0]->IsCrease()),
    false,
    false,
    m_bBoundaryCrease[(q0fvi+3)%4] || (bIsCreaseOrCornerSector && qf0_edges[3]->IsCrease())
  };

  //const bool bStopAtInternalCrease = (false == bIsDartSector);
  const ON_SubDSectorIterator::StopAt stop_at
    = (bIsDartSector)
    ? ON_SubDSectorIterator::StopAt::Boundary
    : ON_SubDSectorIterator::StopAt::AnyCrease
    ;

  if ( false == fsh.ReserveSubDWorkspace( subd_type, N) )
    return ON_SUBD_RETURN_ERROR(false);

  ON_SubDVertex* qv1 = fsh.AllocateVertex(qv0,subd_type,true,N,qv0->m_face_count);
  if ( nullptr == qv1 )
    return ON_SUBD_RETURN_ERROR(false);
  //qv1->m_vertex_facet_type = ON_SubD::VertexFacetType::Quad;
  //qv1->m_vertex_edge_order = ON_SubD::VertexEdgeOrder::radial;

  const ON_SubDEdge* edge0 = sit.CurrentEdge(0);
  if ( nullptr == edge0 )
    return ON_SUBD_RETURN_ERROR(false);

  ON_SubDFace* face_grid1[3][3] = {};
  ON_SubDVertex* vertex_grid1[4][4] = {};
  ON_SubDEdge* edge_grid1[4][2] = {};

  // edge1 = new edge from qv1 to edge0 subdivision point
  ON_SubDEdge* edge1 = ON_SubDQuadFaceTopology_SubdivideEdge(fsh,qv1,qv0,edge0);
  if (nullptr == edge1)
    return ON_SUBD_RETURN_ERROR(false);

  // prepare to rotate coutnerclockwise around qv0, 
  // subdividing edges and adding new faces
  const ON_SubDEdge* e0[2] = {nullptr, edge0};
  ON_SubDEdge* e1[2] = {nullptr, edge1};
  const ON_SubDFace* f0 = qf0;
  ON_SubDFace* f1 = nullptr;
  bool bAtBoundaryCrease = false;
  bool bFinished = false;
  for (unsigned int i = 0; i < N; i++)
  {
    if (nullptr == f0)
      return ON_SUBD_RETURN_ERROR(false);
    e0[0] = e0[1];
    e0[1] = sit.CurrentEdge(1);
    if (nullptr == e0[1])
      return ON_SUBD_RETURN_ERROR(false);
    e1[0] = e1[1];
    if (edge0 == e0[1])
      e1[1] = edge1; // back to where we started
    else
      e1[1] = ON_SubDQuadFaceTopology_SubdivideEdge(fsh, qv1, qv0, e0[1]);
    if (nullptr == e1[1])
      return ON_SUBD_RETURN_ERROR(false);

    f1 = ON_SubDQuadFaceTopology_SubdivideFace(fsh, f0, e1, at_crease_weight);
    if (nullptr == f1 || 4 != f1->m_edge_count || qv1 != f1->Vertex(0))
      return ON_SUBD_RETURN_ERROR(false);

    if (1 == i)
    {
      face_grid1[0][1] = f1;
      vertex_grid1[0][1] = const_cast<ON_SubDVertex*>(f1->Vertex(3));
      vertex_grid1[0][2] = const_cast<ON_SubDVertex*>(f1->Vertex(2));
      edge_grid1[3][0] = const_cast<ON_SubDEdge*>(f1->Edge(1));
      edge_grid1[3][1] = const_cast<ON_SubDEdge*>(f1->Edge(3));
    }

    if (0 == i)
    {
      // central face in new grid
      face_grid1[1][1] = f1;
      vertex_grid1[1][1] = const_cast<ON_SubDVertex*>(f1->Vertex(0));
      vertex_grid1[2][1] = const_cast<ON_SubDVertex*>(f1->Vertex(1));
      vertex_grid1[2][2] = const_cast<ON_SubDVertex*>(f1->Vertex(2));
      vertex_grid1[1][2] = const_cast<ON_SubDVertex*>(f1->Vertex(3));
      if (bBoundaryCrease1[3])
      {
        bAtBoundaryCrease = true;
      }
    }

    if (!bAtBoundaryCrease)
    {
      f0 = sit.NextFace(stop_at);
      if (nullptr == f0)
        bAtBoundaryCrease = true;
      if (e0[1] != sit.CurrentEdge(0))
        return ON_SUBD_RETURN_ERROR(false);
    }

    if (bAtBoundaryCrease)
    {
      e1[1]->m_edge_tag = ON_SubD::EdgeTag::Crease;
      break;
    }

    if (0==i)
      continue;

    if (f0 == qf0 || e0[1] == edge0 || sit.CurrentEdge(0) == edge0)
    {
      // got back to starting face
      // If i+1 < N, it means the vertex is nonmanifold.
      bFinished = (f0 == qf0 && e0[1] == edge0 && sit.CurrentEdge(0) == edge0 && qv1->m_face_count == qv1->m_edge_count);
      break;
    }
  }

  ON_SubDFace* face_grid1_10 = nullptr;

  if (bAtBoundaryCrease)
  {
    if ( qv1->m_face_count < 1 || qv1->m_face_count + 1 != qv1->m_edge_count)
      return ON_SUBD_RETURN_ERROR(false);
    if (true == bBoundaryCrease1[0])
      bFinished = true;
  }
  else if (bFinished)
  {
    face_grid1_10 = f1;
    if ( qv1->m_face_count < 2 || qv1->m_face_count != qv1->m_edge_count)
      return ON_SUBD_RETURN_ERROR(false);
  }
  else
    return ON_SUBD_RETURN_ERROR(false);


  if (bFinished)
  {
    if (4 == qv1->m_edge_count && 4 == qv1->m_face_count)
    {
      f1 = const_cast<ON_SubDFace*>(qv1->m_faces[2]);
      if ( nullptr == f1 || qv1 != f1->Vertex(0) || 4 != f1->m_edge_count)
        return ON_SUBD_RETURN_ERROR(false);
      face_grid1[0][0] = f1;
      vertex_grid1[0][0] = const_cast<ON_SubDVertex*>(f1->Vertex(2));
    }
  }
  else if (false == bBoundaryCrease1[0])
  {
    if ( qf0 != sit.FirstFace())
      return ON_SUBD_RETURN_ERROR(false);
    f0 = sit.PrevFace(stop_at);
    if ( nullptr == f0 )
      return ON_SUBD_RETURN_ERROR(false);
    if ( edge0 != sit.CurrentEdge(1) )
      return ON_SUBD_RETURN_ERROR(false);

    const unsigned int edge_mark = qv1->m_edge_count;

    e0[0] = edge0;
    e0[1] = nullptr;
    e1[0] = edge1;
    e1[1] = nullptr;
    f1 = nullptr;
    for (unsigned int i = 0; i < N - edge_mark; i++)
    {
      e0[1] = e0[0];
      e0[0] = sit.CurrentEdge(0);
      if (nullptr == e0[0])
        return ON_SUBD_RETURN_ERROR(false);
      e1[1] = e1[0];
      e1[0] =  ON_SubDQuadFaceTopology_SubdivideEdge(fsh, qv1, qv0, e0[0]);
      if (nullptr == e1[0])
        return ON_SUBD_RETURN_ERROR(false);

      f1 = ON_SubDQuadFaceTopology_SubdivideFace(fsh, f0, e1, at_crease_weight);
      if (nullptr == f1 || 4 != f1->m_edge_count || qv1 != f1->Vertex(0))
        return ON_SUBD_RETURN_ERROR(false);

      if (0 == i)
        face_grid1_10 = f1;

      f0 = sit.PrevFace(stop_at);
      if (nullptr == f0 || ON_SubD::EdgeTag::Crease == e0[1]->m_edge_tag)
      {
        bFinished = (nullptr == f0 && ON_SubD::EdgeTag::Crease == e0[0]->m_edge_tag && qv1->m_face_count+1 == qv1->m_edge_count);
        if (false == bFinished)
          return ON_SUBD_RETURN_ERROR(false);
        //qv1->m_vertex_edge_order = ON_SubD::VertexEdgeOrder::unset; // edges no longer radially sorted
        break;
      }
    }
  }

  if (false == bFinished)
     return ON_SUBD_RETURN_ERROR(false);

  if (nullptr != face_grid1_10)
  {
    f1 = face_grid1_10;
    if (nullptr == f1 || vertex_grid1[1][1] != f1->Vertex(0) || vertex_grid1[2][1] != f1->Vertex(3) || 4 != f1->m_edge_count)
      return ON_SUBD_RETURN_ERROR(false);
    face_grid1[1][0] = f1;
    vertex_grid1[1][0] = const_cast<ON_SubDVertex*>(f1->Vertex(1));
    vertex_grid1[2][0] = const_cast<ON_SubDVertex*>(f1->Vertex(2));
    edge_grid1[0][0] = const_cast<ON_SubDEdge*>(f1->Edge(0));
    edge_grid1[0][1] = const_cast<ON_SubDEdge*>(f1->Edge(2));
  }

  // Add the 7 remaining elements to vertex_grid1[][]
  if (false == bBoundaryCrease1[0])
  {
    vertex_grid1[3][0] = fsh.AllocateVertex(m_edge_grid[q0fvi][1],ON_SubD::SubDType::QuadCatmullClark,true,2,1);
    if ( nullptr == vertex_grid1[3][0])
      return ON_SUBD_RETURN_ERROR(false);
  }

  vertex_grid1[3][1] = fsh.AllocateVertex(qf0_vertices[1],ON_SubD::SubDType::QuadCatmullClark,true,3,2);
  if ( nullptr == vertex_grid1[3][1])
    return ON_SUBD_RETURN_ERROR(false);


  vertex_grid1[3][2] = fsh.AllocateVertex(qf0_edges[1],ON_SubD::SubDType::QuadCatmullClark,true,3,2);
  if ( nullptr == vertex_grid1[3][2])
    return ON_SUBD_RETURN_ERROR(false);

  vertex_grid1[3][3] = fsh.AllocateVertex(qf0_vertices[2],ON_SubD::SubDType::QuadCatmullClark,true,2,1);
  if ( nullptr == vertex_grid1[3][3])
    return ON_SUBD_RETURN_ERROR(false);

  vertex_grid1[2][3] = fsh.AllocateVertex(qf0_edges[2],ON_SubD::SubDType::QuadCatmullClark,true,3,2);
  if ( nullptr == vertex_grid1[2][3])
    return ON_SUBD_RETURN_ERROR(false);

  vertex_grid1[1][3] = fsh.AllocateVertex(qf0_vertices[3],ON_SubD::SubDType::QuadCatmullClark,true,3,2);
  if ( nullptr == vertex_grid1[1][3])
    return ON_SUBD_RETURN_ERROR(false);

  if (false == bBoundaryCrease1[3])
  {
    vertex_grid1[0][3] = fsh.AllocateVertex(m_edge_grid[(q0fvi+3)%4][0],ON_SubD::SubDType::QuadCatmullClark,true,2,1);
    if ( nullptr == vertex_grid1[0][3])
      return ON_SUBD_RETURN_ERROR(false);
  }

  edge_grid1[1][0] = fsh.AllocateEdge(
    vertex_grid1[2][1], 
    ON_SubDSectorType::IgnoredSectorWeight,
    vertex_grid1[3][1], 
    ON_SubDQuadFaceTopology_CopySectorWeight(qf0_edges[0], qf0_vertices[1])
    );
  if ( nullptr == edge_grid1[1][0])
    return ON_SUBD_RETURN_ERROR(false);

  edge_grid1[1][1] = fsh.AllocateEdge(
    vertex_grid1[2][2], 
    ON_SubDSectorType::IgnoredSectorWeight,
    vertex_grid1[3][2],
    at_crease_weight // ignored unless vertex_grid1[3][2] is tagged as a crease
    );
  if ( nullptr == edge_grid1[1][1])
    return ON_SUBD_RETURN_ERROR(false);

  edge_grid1[2][0] = fsh.AllocateEdge(
    vertex_grid1[2][2], 
    ON_SubDSectorType::IgnoredSectorWeight,
    vertex_grid1[2][3],
    at_crease_weight // ignored unless vertex_grid1[2][3] is tagged as a crease
    );
  if ( nullptr == edge_grid1[2][0])
    return ON_SUBD_RETURN_ERROR(false);

  edge_grid1[2][1] = fsh.AllocateEdge(
    vertex_grid1[1][2],
    ON_SubDSectorType::IgnoredSectorWeight,
    vertex_grid1[1][3],
    ON_SubDQuadFaceTopology_CopySectorWeight(qf0_edges[3], qf0_vertices[3])
    );
  if ( nullptr == edge_grid1[2][1])
    return ON_SUBD_RETURN_ERROR(false);

  // Add the 5 remaining elements to face_grid1[][]
  ON_SubDEdge* fedges[4];
  ON_SubDEdgePtr feptrs[4];
  if (false == bBoundaryCrease1[0])
  {
    fedges[0] = nullptr;
    fedges[1] = nullptr;
    fedges[2] = edge_grid1[1][0];
    fedges[3] = edge_grid1[0][1];

    if (nullptr == fedges[2] || nullptr == fedges[3] )
      return ON_SUBD_RETURN_ERROR(false);

    fedges[0] = fsh.AllocateEdge(
      vertex_grid1[2][0],
      ON_SubDSectorType::IgnoredSectorWeight,
      vertex_grid1[3][0],
      at_crease_weight // ignored unless vertex_grid1[3][0] is tagged as a crease
      );
    if (nullptr == fedges[0])
      return ON_SUBD_RETURN_ERROR(false);
    // m_edge_grid[q0fvi][1]
    fedges[1] = fsh.AllocateEdge(
      vertex_grid1[3][0],
      ON_SubDSectorType::IgnoredSectorWeight,
      vertex_grid1[3][1],
      ON_SubDQuadFaceTopology_CopySectorWeight(m_edge_grid[q0fvi][1], qf0_vertices[1])
      );
    if (nullptr == fedges[1])
      return ON_SUBD_RETURN_ERROR(false);

    feptrs[0] = ON_SubDEdgePtr::Create(fedges[0],0);
    feptrs[1] = ON_SubDEdgePtr::Create(fedges[1],0);
    feptrs[2] = ON_SubDEdgePtr::Create(fedges[2],1);
    feptrs[3] = ON_SubDEdgePtr::Create(fedges[3],1);

    face_grid1[2][0] = fsh.AllocateQuad(zero_face_id, parent_face_id, feptrs);
    if (nullptr == face_grid1[2][0])
      return ON_SUBD_RETURN_ERROR(false);
  }

  // face_grid1[2][1]
  fedges[0] = edge_grid1[1][0];
  fedges[1] = nullptr;
  fedges[2] = edge_grid1[1][1];
  fedges[3] = ON_SUBD_EDGE_POINTER(face_grid1[1][1]->m_edge4[1].m_ptr);

  if (nullptr == fedges[0] || nullptr == fedges[2] || nullptr == fedges[3] )
    return ON_SUBD_RETURN_ERROR(false);

  fedges[1] = fsh.AllocateEdge(
    vertex_grid1[3][1],
    ON_SubDQuadFaceTopology_CopySectorWeight(qf0_edges[1], qf0_vertices[1]),
    vertex_grid1[3][2],
    ON_SubDSectorType::IgnoredSectorWeight
    );
  if (nullptr == fedges[1])
    return ON_SUBD_RETURN_ERROR(false);

  feptrs[0] = ON_SubDEdgePtr::Create(fedges[0],0);
  feptrs[1] = ON_SubDEdgePtr::Create(fedges[1],0);
  feptrs[2] = ON_SubDEdgePtr::Create(fedges[2],1);
  feptrs[3] = ON_SubDEdgePtr::Create(fedges[3],1);

  face_grid1[2][1] = fsh.AllocateQuad(zero_face_id, parent_face_id, feptrs);
  if (nullptr == face_grid1[2][1])
    return ON_SUBD_RETURN_ERROR(false);

  // face_grid1[2][2]
  fedges[0] = edge_grid1[1][1];
  fedges[1] = nullptr;
  fedges[2] = nullptr;
  fedges[3] = edge_grid1[2][0];

  if (nullptr == fedges[0] || nullptr == fedges[3] )
    return ON_SUBD_RETURN_ERROR(false);

  fedges[1] = fsh.AllocateEdge(
    vertex_grid1[3][2],
    ON_SubDSectorType::IgnoredSectorWeight,
    vertex_grid1[3][3],
    ON_SubDQuadFaceTopology_CopySectorWeight(qf0_edges[1], qf0_vertices[2])
    );
  if (nullptr == fedges[1])
    return ON_SUBD_RETURN_ERROR(false);

  fedges[2] = fsh.AllocateEdge(
    vertex_grid1[3][3],
    ON_SubDQuadFaceTopology_CopySectorWeight(qf0_edges[2], qf0_vertices[2]),
    vertex_grid1[2][3],
    ON_SubDSectorType::IgnoredSectorWeight
    );
  if (nullptr == fedges[2])
    return ON_SUBD_RETURN_ERROR(false);

  feptrs[0] = ON_SubDEdgePtr::Create(fedges[0],0);
  feptrs[1] = ON_SubDEdgePtr::Create(fedges[1],0);
  feptrs[2] = ON_SubDEdgePtr::Create(fedges[2],0);
  feptrs[3] = ON_SubDEdgePtr::Create(fedges[3],1);

  face_grid1[2][2] = fsh.AllocateQuad(zero_face_id, parent_face_id, feptrs);
  if (nullptr == face_grid1[2][2])
    return ON_SUBD_RETURN_ERROR(false);

  // face_grid1[1][2]  
  fedges[0] = ON_SUBD_EDGE_POINTER(face_grid1[1][1]->m_edge4[2].m_ptr);
  fedges[1] = edge_grid1[2][0];
  fedges[2] = nullptr;
  fedges[3] = edge_grid1[2][1];

  if (nullptr == fedges[0] || nullptr == fedges[1] || nullptr == fedges[3] )
    return ON_SUBD_RETURN_ERROR(false);

  fedges[2] = fsh.AllocateEdge(
    vertex_grid1[2][3],
    ON_SubDSectorType::IgnoredSectorWeight,
    vertex_grid1[1][3],
    ON_SubDQuadFaceTopology_CopySectorWeight(qf0_edges[2], qf0_vertices[3])
    );
  if (nullptr == fedges[2])
    return ON_SUBD_RETURN_ERROR(false);

  feptrs[0] = ON_SubDEdgePtr::Create(fedges[0],1);
  feptrs[1] = ON_SubDEdgePtr::Create(fedges[1],0);
  feptrs[2] = ON_SubDEdgePtr::Create(fedges[2],0);
  feptrs[3] = ON_SubDEdgePtr::Create(fedges[3],1);

  face_grid1[1][2] = fsh.AllocateQuad(zero_face_id, parent_face_id, feptrs);
  if (nullptr == face_grid1[1][2])
    return ON_SUBD_RETURN_ERROR(false);

  if (false == bBoundaryCrease1[3])
  {
    fedges[0] = edge_grid1[2][1];
    fedges[1] = nullptr;
    fedges[2] = nullptr;
    fedges[3] = edge_grid1[3][0];

    if (nullptr == fedges[0] || nullptr == fedges[3] )
      return ON_SUBD_RETURN_ERROR(false);

    fedges[1] = fsh.AllocateEdge(
      vertex_grid1[1][3],
      ON_SubDQuadFaceTopology_CopySectorWeight(m_edge_grid[(q0fvi+3)%4][0], qf0_vertices[3]),
      vertex_grid1[0][3],
      ON_SubDSectorType::IgnoredSectorWeight
      );
    if (nullptr == fedges[1])
      return ON_SUBD_RETURN_ERROR(false);

    fedges[2] = fsh.AllocateEdge(
      vertex_grid1[0][3],
      at_crease_weight, // ingored unless vertex_grid1[0][3] is tagged as a crease
      vertex_grid1[0][2],
      ON_SubDSectorType::IgnoredSectorWeight
      );
    if (nullptr == fedges[2])
      return ON_SUBD_RETURN_ERROR(false);

    feptrs[0] = ON_SubDEdgePtr::Create(fedges[0],0);
    feptrs[1] = ON_SubDEdgePtr::Create(fedges[1],0);
    feptrs[2] = ON_SubDEdgePtr::Create(fedges[2],0);
    feptrs[3] = ON_SubDEdgePtr::Create(fedges[3],1);

    face_grid1[0][2] = fsh.AllocateQuad(zero_face_id, parent_face_id, feptrs);
    if (nullptr == face_grid1[0][2])
      return ON_SUBD_RETURN_ERROR(false);
  }

  q1ft->m_fsh = &fsh;

  const ON_2dex deltaj = ON_SubDQuadNeighborhood::DeltaDex(q0fvi,0,1);
  ON_2dex dex;
  q1ft->m_face_grid[1][1] = face_grid1[1][1];
  for (unsigned int i = 0; i < 3; i++)
  {
    dex = ON_SubDQuadNeighborhood::GridDex(3, q0fvi, i, 0);
    for (unsigned int j = 0; j < 3; j++)
    {
      q1ft->m_face_grid[dex.i][dex.j] = face_grid1[i][j];
      dex.i += deltaj.i;
      dex.j += deltaj.j;
    }
  }

  for (unsigned int i = 0; i < 4; i++)
  {
    unsigned int j = (q0fvi + i) % 4;
    q1ft->m_bBoundaryCrease[j] = bBoundaryCrease1[i];
    q1ft->m_edge_grid[j][0] = edge_grid1[i][0];
    q1ft->m_edge_grid[j][1] = edge_grid1[i][1];
    q1ft->m_center_edges[j] = face_grid1[1][1]->Edge(i);

    dex = ON_SubDQuadNeighborhood::GridDex(4,q0fvi,i,0);
    for (j = 0; j < 4; j++)
    {
      q1ft->m_vertex_grid[dex.i][dex.j] = vertex_grid1[i][j];
      dex.i += deltaj.i;
      dex.j += deltaj.j;
    }
  }

  q1ft->SetPatchStatus(q0fvi);

  if ( m_bExtraordinaryCornerVertex[q0fvi] )
  {
    // evaluate extraordinary limit point as soon as possible and then save it for future use.
    ON_SubDSectorLimitPoint limit_point;
    const ON_SubD::SubDType subd_type_local_scope = ON_SubD::SubDType::QuadCatmullClark;

    const ON_SubDFace* qv0_sector_face = this->m_face_grid[1][1];
    const ON_SubDFace* qv1_sector_face = q1ft->m_face_grid[1][1];

    if (subd_type_local_scope == qv0->SavedLimitPointType() && qv0->GetLimitPoint(subd_type_local_scope,qv0_sector_face,true,limit_point) && limit_point.IsSet())
    {
      limit_point.m_sector_face = qv1_sector_face; // qv1's sector face
      limit_point.m_next_sector_limit_point = nullptr; // sector checks are required to get "first" face
      qv1->SetSavedLimitPoint(subd_type_local_scope,limit_point);
    }
    else if (qv1->GetLimitPoint(subd_type_local_scope, qv1_sector_face, true, limit_point))
    {
      limit_point.m_sector_face = qv0_sector_face;
      limit_point.m_next_sector_limit_point = nullptr; // sector checks are required to get "first" face
      qv0->SetSavedLimitPoint(subd_type_local_scope,limit_point);
    }
  }

#if defined(ON_DEBUG)
  q1ft->IsValid(); // will trigger a break if "this" is not valid
#endif

  return true;
}


ON_2dex ON_SubDQuadNeighborhood::GridDex(
  unsigned int grid_size,
  unsigned int corner_index,
  unsigned int i,
  unsigned int j
  )
{
  ON_2dex dex;

  switch (corner_index)
  {
  case 1:
    dex.i = grid_size - 1 - j;
    dex.j = i;
    break;
  case 2:
    dex.i = grid_size - 1 - i;
    dex.j = grid_size - 1 - j;
    break;
  case 3:
    dex.i = j;
    dex.j = grid_size - 1 - i;
    break;
  default:
    dex.i = i;
    dex.j = j;
  }

  return dex;
}

ON_2dex ON_SubDQuadNeighborhood::DeltaDex(
  unsigned int corner_index,
  int delta_i,
  int delta_j
  )
{
  ON_2dex deltadex;
  switch (corner_index)
  {
  case 1:
    deltadex.i = -delta_j;
    deltadex.j = delta_i;
    break;
  case 2:
    deltadex.i = -delta_i;
    deltadex.j = -delta_j;
    break;
  case 3:
    deltadex.i = delta_j;
    deltadex.j = -delta_i;
    break;
  default:
    deltadex.i = delta_i;
    deltadex.j = delta_j;
  }

  return deltadex;
}




bool ON_SubDFace::GetQuadLimitSurface(
  size_t limit_surface_cv_stride0,
  size_t limit_surface_cv_stride1,
  double* limit_surface_cv
  ) const
{
  double srf_cv[4][4][3];

  if ( 4 != m_edge_count)
    return false;

  ON_SubDQuadNeighborhood qft;
  if (false == qft.Set(this ))
    return false;

  if ( false == qft.m_bIsCubicPatch )
    return false;

  if (false == qft.GetLimitSurfaceCV(&srf_cv[0][0][0], 4U))
    return false;

  for (unsigned int i = 0; i < 4; i++)
  {
    double* dst_cv = limit_surface_cv + i*limit_surface_cv_stride0;
    for (unsigned int j = 0; j < 4; j++)
    {
      const double* src_cv = srf_cv[i][j];
      dst_cv[0] = src_cv[0];
      dst_cv[1] = src_cv[1];
      dst_cv[2] = src_cv[2];

      dst_cv += limit_surface_cv_stride1;
    }
  }

  return true;
}

bool ON_SubDFace::GetQuadLimitSurface(
class ON_NurbsSurface& nurbs_surface
  ) const
{
  if (false == nurbs_surface.Create(
    3, // dim
    false, // is_rat
    4, 4, // orders
    4, 4  // cv_counts
    ))
  {
    return false;
  }
  if (false == GetQuadLimitSurface(nurbs_surface.m_cv_stride[0], nurbs_surface.m_cv_stride[1], nurbs_surface.m_cv))
    return false;

  // evaluation domain will be [0,1] x [0,1]
  double k = -2.0;
  for (unsigned int i = 0; i < 6; i++)
  {
    nurbs_surface.m_knot[0][i] = nurbs_surface.m_knot[1][i] = k;
    k += 1.0;
  }

  return true;
}

bool ON_SubDFace::GetQuadLimitSurface(
class ON_BezierSurface& bezier_surface
  ) const
{
  if (false == bezier_surface.Create(
    3, // dim
    false, // is_rat
    4, 4 // orders
    ))
    return false;

  double knots[2][6] = { { -2.0, -1.0, 0.0, 1.0, 2.0, 3.0 }, { -2.0, -1.0, 0.0, 1.0, 2.0, 3.0 } };

  ON_NurbsSurface nurbs_surface;
  nurbs_surface.m_dim = 3;
  nurbs_surface.m_is_rat = false;
  nurbs_surface.m_order[0] = 4;
  nurbs_surface.m_order[1] = 4;
  nurbs_surface.m_cv_count[0] = 4;
  nurbs_surface.m_cv_count[1] = 4;
  nurbs_surface.m_cv_stride[0] = bezier_surface.m_cv_stride[0];
  nurbs_surface.m_cv_stride[0] = bezier_surface.m_cv_stride[0];
  nurbs_surface.m_cv = bezier_surface.m_cv;
  nurbs_surface.m_cv_capacity = 0;
  nurbs_surface.m_knot[0] = knots[0];
  nurbs_surface.m_knot[1] = knots[1];
  nurbs_surface.m_knot_capacity[0] = 0;
  nurbs_surface.m_knot_capacity[1] = 0;

  if (false == GetQuadLimitSurface(nurbs_surface))
    return false;

  if (false == nurbs_surface.ClampEnd(0, 2))
    return false;
  if (false == nurbs_surface.ClampEnd(1, 2))
    return false;

  return true;
}




ON_SubDFaceNeighborhood::~ON_SubDFaceNeighborhood()
{
  ReserveCapacity(ON_SubD::SubDType::Unset,nullptr);
}

bool ON_SubDFaceNeighborhood::ReserveCapacity(
  ON_SubD::SubDType subd_type,
  const ON_SubDFace* face
  )
{
  m_face0 = nullptr;
  m_subd_type = ON_SubD::SubDType::Unset;
  m_center_vertex1 = nullptr;
  m_face1_count = 0;
  m_face1 = nullptr;

  unsigned int v_capacity =  0;
  unsigned int e_capacity =  0;
  unsigned int f_capacity =  0;
  unsigned int a_capacity =  0;
  
  for (;;)
  {
    if (nullptr == face)
      break;

    const unsigned int N = face->m_edge_count;
    if (N <= 2)
      break;

    // ordinary valence
    //const unsigned short V0 
    //  = (ON_SubD::FacetType::Quad == ON_SubD::FacetTypeFromSubDType(subd_type))
    //  ? 4
    //  : 6;
    // set E = extraordinary vertex valence overhead
    unsigned int S = 0;
    //unsigned int E = 0;
    const ON_SubDEdgePtr* edges = face->m_edge4;
    ON__UINT_PTR edge_ptr;
    const ON_SubDEdge* edge;
    const ON_SubDVertex* vertex;
    unsigned int i;
    for (i = 0; i < N; i++, edges++)
    {
      if (4 == i)
      {
        if (nullptr == face->m_edgex)
          return ON_SUBD_RETURN_ERROR(false);
        edges = face->m_edgex;
      }
      edge_ptr = edges->m_ptr;
      edge = ON_SUBD_EDGE_POINTER(edge_ptr);
      if (nullptr == edge)
        break;
      vertex = edge->m_vertex[ON_SUBD_EDGE_DIRECTION(edge_ptr)];
      if (nullptr == vertex)
        break;
      if (vertex->m_edge_count < 2 )
        break;
      if (vertex->m_edge_count < vertex->m_face_count )
        break;
      S += vertex->m_edge_count;
      //if (vertex->m_edge_count > V0 )
      //  E += (vertex->m_edge_count - V0);
    }
    if (i != N)
      break;

    if (ON_SubD::SubDType::QuadCatmullClark == subd_type)
    {
      f_capacity =  S;
      e_capacity =  3*S - N;
      v_capacity =  2*(S - N) + 1;
      a_capacity =  4*f_capacity + 2*e_capacity + 2*v_capacity;
    }
    else if (ON_SubD::SubDType::TriLoopWarren == subd_type)
    {
      // todo -- add tri support
      // (remember to add 4 to a_capacity for the ON_SubDFaceNeighborhood.m_face1[] array
      //  when N = 3).
      break;
    }
    else
    {
      break;
    }

    return m_fsh.ReserveSubDWorkspace(v_capacity, e_capacity, f_capacity, a_capacity);
  }

  m_fsh.ReserveSubDWorkspace(0,0,0,0);
  if (ON_SubD::SubDType::Unset == subd_type && nullptr == face )
    return true;
  return ON_SUBD_RETURN_ERROR(false);
}


bool ON_SubDFaceNeighborhood::Subdivide(
  ON_SubD::SubDType subd_type,
  const ON_SubDFace* face
  )
{
  if (false == ReserveCapacity(subd_type, face))
    return ON_SUBD_RETURN_ERROR(false);

  if (ON_SubD::SubDType::QuadCatmullClark == subd_type)
    return ON_SubDFaceNeighborhood::QuadSubdivideHelper(face);

  if (ON_SubD::SubDType::TriLoopWarren == subd_type)
    return ON_SubDFaceNeighborhood::TriSubdivideHelper(face);

  return ON_SUBD_RETURN_ERROR(false);
}


bool ON_SubDFaceNeighborhood::TriSubdivideHelper(
  const ON_SubDFace* face
  )
{
  // todo - add tri support
  return ON_SUBD_RETURN_ERROR(false);
}

////static bool RadialSort(
////  unsigned int vertex1_sort_mark,
////  ON_SubDVertex* vertex
////  )
////{
////  if (nullptr == vertex || vertex->m_face_count > vertex->m_edge_count)
////    return ON_SUBD_RETURN_ERROR(false);
////
////  if ( 0 == vertex1_sort_mark)
////    return true;
////
////  unsigned int e0_count = vertex1_sort_mark+1;
////  unsigned int f0_count= vertex1_sort_mark;
////  unsigned int e_count = vertex->m_edge_count;
////  unsigned int f_count = vertex->m_face_count;
////  if (e0_count > e_count || f0_count > f_count)
////    return ON_SUBD_RETURN_ERROR(false);
////
////  ON__UINT_PTR stack_buffer[40];
////  ON__UINT_PTR* buffer = 0;
////  if (e0_count <= sizeof(stack_buffer) / sizeof(stack_buffer[0]))
////    buffer = stack_buffer;
////  else
////  {
////    buffer = new (std::nothrow) ON__UINT_PTR[e0_count];
////    if ( nullptr == buffer)
////      return ON_SUBD_RETURN_ERROR(false);
////  }
////
////  unsigned int i, j;
////  ON__UINT_PTR* a;
////  
////  a = (ON__UINT_PTR*)vertex->m_edges;
////  for (i = 0; i < e0_count; i++)
////  {
////    buffer[i] = a[i];
////  }
////  j = 0;
////  for (i = e0_count; i < e_count; i++)
////  {
////    a[j++] = a[i];
////  }
////  for (i = 0; i < e0_count; i++)
////  {
////    a[j++] = buffer[i];
////  }
////
////  a = (ON__UINT_PTR*)vertex->m_faces;
////  for (i = 0; i < f0_count; i++)
////  {
////    buffer[i] = a[i];
////  }
////  j = 0;
////  for (i = f0_count; i < f_count; i++)
////  {
////    a[j++] = a[i];
////  }
////  for (i = 0; i < f0_count; i++)
////  {
////    a[j++] = buffer[i];
////  }
////
////  if ( buffer != stack_buffer)
////    delete[] buffer;
////  vertex->m_vertex_edge_order = ON_SubD::VertexEdgeOrder::radial;
////  return true;
////}


#if defined(ON_DEBUG)

//// debugging tool. If a call to this function is left in release code, the compile will fail (on purpose).
//static void ON_DEBUG_SubDBreakPoint(const ON_SubDFace* face)
//{
//  for (;;)
//  {
//    if (nullptr == face)
//      break;
//    if (0 != face->m_level)
//      break;
//    if (34 != face->m_id)
//      break;
//    ON_TextLog::Null.Print("Breakpoint here."); // does nothing prevents warning as error 
//    break;
//  }
//#if !defined(ON_DEBUG)
//#error Do not use ON_DEBUG_SubDBreakPoint() in release builds.
//#endif
//}

#endif

bool ON_SubDFaceNeighborhood::QuadSubdivideHelper(
  const ON_SubDFace* face
  )
{
  // input face is valid and space is reserved.
  //ON_DEBUG_SubDBreakPoint(face);


  const ON_SubD::SubDType subd_type = ON_SubD::SubDType::QuadCatmullClark;
  
  // When a smooth subdivision edge ends at a vertex that is a subdivision point
  // of a creased original edge, this is the value to assign to the new
  // edge's m_vertex_weight. The "2" is there because there would be 2
  // sector faces if the subdivision was complete.
  const double at_crease2_weight = ON_SubDSectorType::CreaseSectorWeight(subd_type,2);

  const unsigned int N = face->m_edge_count;

  const unsigned int zero_face_id = face->m_zero_face_id;
  const unsigned int parent_face_id = face->m_parent_face_id;

  const bool bUseSavedSubdivisionPoint = true;

  ON_SubDSectorLimitPoint limit_point;

  // create central vertex
  ON_SubDVertex* center_vertex1 = m_fsh.AllocateVertex(face,subd_type,bUseSavedSubdivisionPoint,N,N);
  if ( nullptr == center_vertex1)
    return ON_SUBD_RETURN_ERROR(false);

  const ON_SubDVertex* vertex0 = face->Vertex(0);
  if ( nullptr == vertex0 )
    return ON_SUBD_RETURN_ERROR(false);
  const bool bFirstVertexHasValence2 = (2 == vertex0->m_edge_count && 2 == vertex0->m_face_count && vertex0->IsSmoothOrDart());

  const ON_SubDEdge* edge0 = nullptr;
  ON__UINT_PTR edge0_dir = 0;
  ON_SubDVertex* vertex1 = nullptr;
  ON_SubDEdge* edge1 = nullptr;

  // Calculate 2*N subdivison vertices on the boundary of input "face"
  // and N subdivision edge that radiate from center_vertex1 to the input face edge's subdivison points.
  // This loop also vertifies that all input vertex and edge pointers are not null and have the
  // expected properties so the rest of this function can dispense with checking.
  const ON_SubDEdgePtr* face_m_edges = face->m_edge4;
  for (unsigned int i = 0; i < N; i++, face_m_edges++)
  {
    if (4 == i)
    {
      if (nullptr == face->m_edgex)
        return ON_SUBD_RETURN_ERROR(false);
      face_m_edges = face->m_edgex;
    }
    const ON__UINT_PTR edge0_ptr = face_m_edges->m_ptr;

    edge0 = ON_SUBD_EDGE_POINTER(edge0_ptr);
    if (nullptr == edge0 || nullptr == edge0->m_vertex[0] || nullptr == edge0->m_vertex[1])
      return ON_SUBD_RETURN_ERROR(false);
    edge0_dir = ON_SUBD_EDGE_DIRECTION(edge0_ptr);    
    vertex0 = edge0->m_vertex[edge0_dir];
    if (vertex0->m_edge_count < 2)
      return ON_SUBD_RETURN_ERROR(false);
   
    // One of the main reasons for creating a ON_SubDFaceNeighborhood is to calcualtethe 
    // limit mesh and limit cubic surfaces when the original face is not a quad.  
    // For these calculations, we need to calculate and save the limit point for extraordinary
    // verticies while enough information is available to calculate it.  Doing the calculation
    // before calling m_fsh.AllocateVertex(), insures the information will be copied to vertex1.
    if ( false == vertex0->GetLimitPoint(subd_type,face,true,limit_point) )
      return ON_SUBD_RETURN_ERROR(false);
    vertex1 = m_fsh.AllocateVertex(vertex0,subd_type,bUseSavedSubdivisionPoint,vertex0->m_edge_count,vertex0->m_edge_count);
    if ( nullptr == vertex1)
      return ON_SUBD_RETURN_ERROR(false);
    if (nullptr != limit_point.m_sector_face || subd_type != vertex1->SavedLimitPointType() )
    {
      // While there may be multiple sectors around vertex0, the only limit point 
      // that matters is this local subdivision is the one for vertex0 in the sector containing the input face.
      limit_point.m_next_sector_limit_point = (ON_SubDSectorLimitPoint*)1; // causes unnecessary test to be skipped
      limit_point.m_sector_face = nullptr;
      vertex1->SetSavedLimitPoint(subd_type, limit_point);
    }

    // This vertex is either a crease (3 edges, 2 faces) or a smooth ordinary vertex (4 edges, 4 faces).
    vertex1 = m_fsh.AllocateVertex(edge0,subd_type,bUseSavedSubdivisionPoint,4,4);
    if ( nullptr == vertex1)
      return ON_SUBD_RETURN_ERROR(false);

    edge1 = m_fsh.AllocateEdge(
      center_vertex1,
      ON_SubDSectorType::IgnoredSectorWeight,
      vertex1,
      at_crease2_weight // ingored unless vertex1 is tagged as a crease
      );
    if ( nullptr == edge1)
      return ON_SUBD_RETURN_ERROR(false);
  }

  // ring_vertex1 and last_ring_vertex1 are used to repeatedly iterate through subdivsion vertices on the boundary 
  // of the original face.
  // i = "corner" index (= <= i < N.
  // ring_vertex1[3] = last vertex in the boundary and is used for initialization when i = 0.
  // ring_vertex1[0] = subdivision vertex on input face->Edge(i-1)
  // ring_vertex1[1] = subdivision vertex on input face->Vertex(i)
  // ring_vertex1[2] = subdivision vertex on input face->Edge(i)
  ON_SubDVertex* ring_vertex1[4] = { nullptr, nullptr, nullptr, vertex1 };


  // Calculate the 2*N subdivison edges on the boundary of input "face"
  // and N subdivision faces.
  ON_SubDFace* face1 = nullptr;
  ON_SubDEdgePtr face1_eptrs[4] = {ON_SubDEdgePtr::Null,ON_SubDEdgePtr::Null,ON_SubDEdgePtr::Null,ON_SubDEdgePtr::Create(edge1, 1)};
  face_m_edges = face->m_edge4;
  for (unsigned int i = 0; i < N; i++, face_m_edges++)
  {
    if (4 == i)
      face_m_edges = face->m_edgex;
    const ON__UINT_PTR edge0_ptr = face_m_edges->m_ptr;

    const ON_SubDEdge* prev_edge0 = edge0;
    //const ON__UINT_PTR prev_edge0_dir = edge0_dir;
    edge0 = ON_SUBD_EDGE_POINTER(edge0_ptr);
    edge0_dir = ON_SUBD_EDGE_DIRECTION(edge0_ptr);
    vertex0 = edge0->m_vertex[edge0_dir];

    // ring_vertex1[0] = subdivision vertex on input face->Edge(i-1) = prev_edge0
    // ring_vertex1[1] = subdivision vertex on input face->Vertex(i) = vertex0
    // ring_vertex1[2] = subdivision vertex on input face->Edge(i) = edge0
    if (0 == i)
    {
      ring_vertex1[0] = ring_vertex1[3];
      ring_vertex1[1] = const_cast<ON_SubDVertex*>(center_vertex1->m_next_vertex);
      ring_vertex1[2] = const_cast<ON_SubDVertex*>(ring_vertex1[1]->m_next_vertex);
    }
    else
    {
      ring_vertex1[0] = ring_vertex1[2];
      ring_vertex1[1] = const_cast<ON_SubDVertex*>(ring_vertex1[0]->m_next_vertex);
      ring_vertex1[2] = const_cast<ON_SubDVertex*>(ring_vertex1[1]->m_next_vertex);
    }

    face1_eptrs[0] = face1_eptrs[3].Reversed();
    face1_eptrs[3] = center_vertex1->m_edges[i].Reversed();

    edge1 = m_fsh.AllocateEdge(
      ring_vertex1[0],
      ON_SubDSectorType::IgnoredSectorWeight,
      ring_vertex1[1],
      ON_SubDQuadFaceTopology_CopySectorWeight(prev_edge0, vertex0)
      );
    if ( nullptr == edge1 )
      return ON_SUBD_RETURN_ERROR(false);
    face1_eptrs[1] = ON_SubDEdgePtr::Create(edge1, 0);


    edge1 = m_fsh.AllocateEdge(
      ring_vertex1[1],
      ON_SubDQuadFaceTopology_CopySectorWeight(edge0, vertex0),
      ring_vertex1[2],
      ON_SubDSectorType::IgnoredSectorWeight
      );
    if ( nullptr == edge1 )
      return ON_SUBD_RETURN_ERROR(false);
    face1_eptrs[2] = ON_SubDEdgePtr::Create(edge1, 0);

    face1 = m_fsh.AllocateQuad(zero_face_id, parent_face_id, face1_eptrs);
    if ( nullptr == face1)
      return ON_SUBD_RETURN_ERROR(false);
  }

  /////////////////////////////////////////////////////////////////////////////////
  // First, radially sort the subdivision vertex edge lists.
  // This sorting is required for calculations later in this function.
  //
  // Then, add a subdivision edge from the input face's edge's subdivision point ("ring_vertex1")
  // to the neighboring "level 0" face subdivision point. When this subdivision edge
  // is added, it is critical below that it be in ring_vertex1->m_edges[3]
  //
  face_m_edges = face->m_edge4;
  for (unsigned int i = 0; i < N; i++, face_m_edges++)
  {
    if (4 == i)
      face_m_edges = face->m_edgex;
    const ON__UINT_PTR edge0_ptr = face_m_edges->m_ptr;
    edge0 = ON_SUBD_EDGE_POINTER(edge0_ptr);
    edge0_dir = ON_SUBD_EDGE_DIRECTION(edge0_ptr);
    vertex0 = edge0->m_vertex[edge0_dir];

    // ring_vertex1[0] = subdivision vertex on input face->Edge(i-1)
    // ring_vertex1[1] = subdivision vertex on input face->Vertex(i) = vertex0
    // ring_vertex1[2] = subdivision vertex on input face->Edge(i) = edge0
    if (0 == i)
    {
      ring_vertex1[0] = ring_vertex1[3];
      ring_vertex1[1] = const_cast<ON_SubDVertex*>(center_vertex1->m_next_vertex);
      ring_vertex1[2] = const_cast<ON_SubDVertex*>(ring_vertex1[1]->m_next_vertex);
    }
    else
    {
      ring_vertex1[0] = ring_vertex1[2];
      ring_vertex1[1] = const_cast<ON_SubDVertex*>(ring_vertex1[0]->m_next_vertex);
      ring_vertex1[2] = const_cast<ON_SubDVertex*>(ring_vertex1[1]->m_next_vertex);
    }


    // debugggin checks.
    // ring_vertex1[0] counts vary
    if ( 2 != ring_vertex1[1]->m_edge_count || 1 != ring_vertex1[1]->m_face_count)
      return ON_SUBD_RETURN_ERROR(false);
    if ( 3 !=  ring_vertex1[2]->m_edge_count || 2 !=  ring_vertex1[2]->m_face_count )
      return ON_SUBD_RETURN_ERROR(false);

    // swap edges at the corner vertex
    face1_eptrs[0] = ring_vertex1[1]->m_edges[0];
    ring_vertex1[1]->m_edges[0] = ring_vertex1[1]->m_edges[1];
    ring_vertex1[1]->m_edges[1] = face1_eptrs[0];

    if ((N-1) == i)
    {
      face1_eptrs[0] = ring_vertex1[2]->m_edges[1];
      face1_eptrs[1] = ring_vertex1[2]->m_edges[0];
      face1_eptrs[2] = ring_vertex1[2]->m_edges[2];
    }
    else
    {
      face1_eptrs[0] = ring_vertex1[2]->m_edges[2];
      face1_eptrs[1] = ring_vertex1[2]->m_edges[0];
      face1_eptrs[2] = ring_vertex1[2]->m_edges[1];
    }
    ring_vertex1[2]->m_edges[0] = face1_eptrs[0];
    ring_vertex1[2]->m_edges[1] = face1_eptrs[1];
    ring_vertex1[2]->m_edges[2] = face1_eptrs[2];

    if (bFirstVertexHasValence2)
      continue;

    const ON_SubDFace* neighbor_face0 = edge0->NeighborFacePtr(face, false).Face();
    if (nullptr == neighbor_face0)
    {
      if (false == edge0->IsHardCrease())
      {
        // Either input face or edge0 is damaged, but this error can be tolerated.
        ON_SubDIncrementErrorCount();
      }
      continue;
    }
    vertex1 = nullptr;
    if (i > 0 && 2 == vertex0->m_edge_count && 2 == vertex0->m_face_count && 4 == ring_vertex1[0]->m_edge_count)
    {
      // uncommon valence 2 case that can be handled here
      edge1 = ON_SUBD_EDGE_POINTER(ring_vertex1[0]->m_edges[3].m_ptr);
      if ( nullptr == edge1 )
        return ON_SUBD_RETURN_ERROR(false);
      vertex1 = const_cast<ON_SubDVertex*>(edge1->m_vertex[1]);
      if (nullptr == vertex1)
        return ON_SUBD_RETURN_ERROR(false);
    }
    if (nullptr == vertex1)
    {
      vertex1 = m_fsh.AllocateVertex(neighbor_face0, subd_type, bUseSavedSubdivisionPoint, 4, 2);
      if (nullptr == vertex1)
        return ON_SUBD_RETURN_ERROR(false);
    }
    edge1 = m_fsh.AllocateEdge(
      ring_vertex1[2],
      at_crease2_weight, // ingored unless ring_vertex1[0] is tagged as a crease
      vertex1,
      ON_SubDSectorType::IgnoredSectorWeight
      );
    if (nullptr == edge1)
      return ON_SUBD_RETURN_ERROR(false);
  }

  if (bFirstVertexHasValence2)
  {
    // extremely uncommon case that requires this mess ...
    ON_SimpleArray<const ON_SubDFace*> neighbors(N);
    face_m_edges = face->m_edge4;
    for (unsigned int i = 0; i < N; i++, face_m_edges++)
    {
      if (4 == i)
        face_m_edges = face->m_edgex;
      const ON__UINT_PTR edge0_ptr = face_m_edges->m_ptr;
      edge0 = ON_SUBD_EDGE_POINTER(edge0_ptr);
      neighbors.Append(edge0->NeighborFacePtr(face, edge0->IsHardCrease()).Face());
    }

    ON_SimpleArray<ON_SubDVertex*> neighbors_vertex1(N);
    face_m_edges = face->m_edge4;
    for (unsigned int i = 0; i < N; i++, face_m_edges++)
    {
      if (4 == i)
        face_m_edges = face->m_edgex;
      const ON__UINT_PTR edge0_ptr = face_m_edges->m_ptr;
      edge0 = ON_SUBD_EDGE_POINTER(edge0_ptr);
      if (0 == i)
      {
        ring_vertex1[0] = ring_vertex1[3];
        ring_vertex1[1] = const_cast<ON_SubDVertex*>(center_vertex1->m_next_vertex);
        ring_vertex1[2] = const_cast<ON_SubDVertex*>(ring_vertex1[1]->m_next_vertex);
      }
      else
      {
        ring_vertex1[0] = ring_vertex1[2];
        ring_vertex1[1] = const_cast<ON_SubDVertex*>(ring_vertex1[0]->m_next_vertex);
        ring_vertex1[2] = const_cast<ON_SubDVertex*>(ring_vertex1[1]->m_next_vertex);
      }


      const ON_SubDFace* neighbor_face0 = edge0->NeighborFacePtr(face, edge0->IsHardCrease()).Face();
      if (nullptr == neighbor_face0)
      {
        neighbors_vertex1.Append(nullptr);
        continue;
      }
      for (unsigned int j = 0; j < i; j++)
      {
        if (neighbor_face0 == neighbors[j])
        {
          vertex1 = neighbors_vertex1[j];
          break;
        }
      }
      if (nullptr == vertex1)
      {
        vertex1 = m_fsh.AllocateVertex(neighbor_face0, subd_type, bUseSavedSubdivisionPoint, 4, 2);
        if (nullptr == vertex1)
          return ON_SUBD_RETURN_ERROR(false);
      }
      neighbors_vertex1.Append(vertex1);
      edge1 = m_fsh.AllocateEdge(
        ring_vertex1[2],
        at_crease2_weight, // ingored unless ring_vertex1[0] is tagged as a crease
        vertex1,
        ON_SubDSectorType::IgnoredSectorWeight
      );
      if (nullptr == edge1)
        return ON_SUBD_RETURN_ERROR(false);
    }
  }

  /////////////////////////////////////////////////////////////////////////////////
  //
  // At each corner of the original face, add the outer subdivision quads as needed.
  //
  const ON_SubDEdge* edge0_duo[2] = {nullptr, face->Edge(N-1) };
  const ON_SubDFace* neighbor0_duo[2] = {nullptr, edge0_duo[1]->NeighborFace(face,false) };
  bool edge0_duo_bIsHardCrease[2] = { false, edge0_duo[1]->IsHardCrease() };
  bool edge0_duo_bIsDartCrease[2] = { false, edge0_duo_bIsHardCrease[1] ? false : edge0_duo[1]->IsDartCrease() };
  ON_SubDEdge* edge1_quartet[4] = {nullptr,nullptr,nullptr, ((4==ring_vertex1[2]->m_edge_count)?(ON_SUBD_EDGE_POINTER(ring_vertex1[2]->m_edges[3].m_ptr)):nullptr) };
  ON_SubDSectorIterator sit;
  face_m_edges = face->m_edge4;
  for (unsigned int i = 0; i < N; i++, face_m_edges++)
  {
    if (4 == i)
      face_m_edges = face->m_edgex;

    // edge0_duo[0] = face->Edge(i-1)
    // edge0_duo[1] = face->Edge(i)
    edge0_duo[0] = edge0_duo[1];
    edge0_duo[1] = ON_SUBD_EDGE_POINTER(face_m_edges->m_ptr);

    // vertex0 = face->Vertex(i)
    vertex0 = edge0_duo[1]->m_vertex[ON_SUBD_EDGE_DIRECTION(face_m_edges->m_ptr)];
    //const bool bCornerVertexIsDart = vertex0->IsDart();
    //const bool bCornerVertexIsCreaseOrCorner = bCornerVertexIsDart ? false : vertex0->IsCreaseOrCorner();

    edge0_duo_bIsHardCrease[0] = edge0_duo_bIsHardCrease[1];
    edge0_duo_bIsDartCrease[0] = edge0_duo_bIsDartCrease[1];
    edge0_duo_bIsHardCrease[1] = edge0_duo[1]->IsHardCrease();
    edge0_duo_bIsDartCrease[1] = edge0_duo_bIsHardCrease[1] ? false : edge0_duo[1]->IsDartCrease();
    //const bool bDartCreaseSituation = edge0_duo_bIsDartCrease[0] || edge0_duo_bIsDartCrease[1];

    // neighbor0_duo[0] = original face neighbor across edge0_duo[0]
    // neighbor0_duo[1] = original face neighbor across edge0_duo[1]
    neighbor0_duo[0] = neighbor0_duo[1];
    neighbor0_duo[1] = edge0_duo[1]->NeighborFace(face, false);

    // ring_vertex1[0] = subdivision vertex on input face->Edge(i-1) = edge0_duo[0]
    // ring_vertex1[1] = subdivision vertex on input face->Vertex(i) = vertex0
    // ring_vertex1[2] = subdivision vertex on input face->Edge(i) = edge0_duo[1]
    if (0 == i)
    {
      ring_vertex1[0] = ring_vertex1[3];
      ring_vertex1[1] = const_cast<ON_SubDVertex*>(center_vertex1->m_next_vertex);
      ring_vertex1[2] = const_cast<ON_SubDVertex*>(ring_vertex1[1]->m_next_vertex);
    }
    else
    {
      ring_vertex1[0] = ring_vertex1[2];
      ring_vertex1[1] = const_cast<ON_SubDVertex*>(ring_vertex1[0]->m_next_vertex);
      ring_vertex1[2] = const_cast<ON_SubDVertex*>(ring_vertex1[1]->m_next_vertex);
    }
    
    // edge1_quartet[0] = null or subdivision edge from ring_vertex1[0] to neighbor0_duo[0] subdivision point
    // edge1_quartet[1] = subdivision edge from ring_vertex1[0] to ring_vertex1[1]
    // edge1_quartet[2] = subdivision edge from ring_vertex1[1] to ring_vertex1[2]
    // edge1_quartet[3] = null or subdivision edge from ring_vertex1[2] to neighbor0_duo[1] subdivision point
    edge1_quartet[0] = edge1_quartet[3];
    edge1_quartet[1] = ON_SUBD_EDGE_POINTER(ring_vertex1[1]->m_edges[1].m_ptr);
    edge1_quartet[2] = ON_SUBD_EDGE_POINTER(ring_vertex1[1]->m_edges[0].m_ptr);
    edge1_quartet[3] = (4==ring_vertex1[2]->m_edge_count) ? (ON_SUBD_EDGE_POINTER(ring_vertex1[2]->m_edges[3].m_ptr)) : nullptr;
       
    if (edge0_duo_bIsHardCrease[0] && edge0_duo_bIsHardCrease[1])
    {
      // no outer quads at this corner
      continue;
    }

    if ( false == edge0_duo_bIsHardCrease[0] && false == edge0_duo_bIsDartCrease[0] && false == edge0_duo[0]->IsSmooth() )
    {
      // This is an error condition that we can tolerate and still get a partial result.
      ON_SubDIncrementErrorCount();
      continue;
    }

    if ( false == edge0_duo_bIsHardCrease[1] && false == edge0_duo_bIsDartCrease[1] && false == edge0_duo[1]->IsSmooth() )
    {
      // This is an error condition that we can tolerate and still get a partial result.
      ON_SubDIncrementErrorCount();
      continue;
    }

    if (nullptr == neighbor0_duo[0] || nullptr == edge1_quartet[0])
    {
      if (false == edge0_duo_bIsHardCrease[0])
      {
        // This is an error condition that we can tolerate and still get a partial result.
        ON_SubDIncrementErrorCount();
        continue;
      }
    }

    if (nullptr == neighbor0_duo[1] || nullptr == edge1_quartet[3])
    {
      if (false == edge0_duo_bIsHardCrease[1])
      {
        // This is an error condition that we can tolerate and still get a partial result.
        ON_SubDIncrementErrorCount();
        continue;
      }
    }

    if (neighbor0_duo[0] == neighbor0_duo[1])
    {
      // special case
      if ( nullptr == neighbor0_duo[0] || 2 == vertex0->m_edge_count)
      {
        // This is an error condition that we can tolerate and still get a partial result.
        ON_SubDIncrementErrorCount();
        continue;
      }
      if (nullptr == edge1_quartet[0] || nullptr == edge1_quartet[3] || edge1_quartet[0]->m_vertex[0] != edge1_quartet[3]->m_vertex[0] )
      {
        // This is an error condition that we can tolerate and still get a partial result.
        ON_SubDIncrementErrorCount();
        continue;
      }
      continue;
    }

    if (vertex0->m_face_count <= 1 || vertex0->m_edge_count <= 2)
    {
      // This is an error condition that we can tolerate and still get a partial result.
      ON_SubDIncrementErrorCount();
      continue;
    }

    /////////////////////////////////////////////////////////////////////////////////
    //
    // There is at least one outer subdivision quads around the inner corner subd quad at face->Vertex(i)

    if (2 == vertex0->m_edge_count && 2 == vertex0->m_face_count)
    {
      // valance 2 special case
      face1_eptrs[0] = ON_SubDEdgePtr::Create(edge1_quartet[2],1);
      face1_eptrs[1] = ON_SubDEdgePtr::Create(edge1_quartet[3],0);
      face1_eptrs[2] = ON_SubDEdgePtr::Create(edge1_quartet[0],1);
      face1_eptrs[3] = ON_SubDEdgePtr::Create(edge1_quartet[1],1);
      face1 = m_fsh.AllocateQuad(zero_face_id, parent_face_id, face1_eptrs);
      if ( nullptr == face1)
        return ON_SUBD_RETURN_ERROR(false);
      continue;
    }

    if ( vertex0 != sit.Initialize(face,0,i) )
      return ON_SUBD_RETURN_ERROR(false);

    if (
      vertex0 != sit.CenterVertex()
      || face != sit.CurrentFace()
      || (edge0_duo[0] != sit.CurrentEdge(1))
      || (edge0_duo[1] != sit.CurrentEdge(0))
      )
    {
      return ON_SUBD_RETURN_ERROR(false);
    }


    const unsigned int vertex_face_count = vertex0->m_face_count;
    const ON_SubDFace* face0 = nullptr;

    ON_SubDVertex* face1_corners[4] = {ring_vertex1[1],nullptr,nullptr,nullptr};

    if (vertex0->IsCreaseOrCorner() && edge0_duo_bIsDartCrease[0] && edge0_duo_bIsDartCrease[1])
    {
      // special case
      if ( vertex_face_count < 3 )
        return ON_SUBD_RETURN_ERROR(false);
      if ( nullptr == neighbor0_duo[0] || nullptr == neighbor0_duo[1] )
        return ON_SUBD_RETURN_ERROR(false);

      face0 = sit.PrevFace(ON_SubDSectorIterator::StopAt::HardCrease);
      if ( face0 != neighbor0_duo[1] )
        return ON_SUBD_RETURN_ERROR(false);
      edge0 = sit.CurrentEdge(0);
      if ( nullptr == edge0 )
        return ON_SUBD_RETURN_ERROR(false);

      const bool b3FaceCase = (neighbor0_duo[0] == edge0->NeighborFace(face0, false));
      
      face1_corners[1] = m_fsh.AllocateVertex(edge0,subd_type,bUseSavedSubdivisionPoint,3,2);
      face1_corners[2] = const_cast<ON_SubDVertex*>(edge1_quartet[3]->m_vertex[1]);
      face1_corners[3] = ring_vertex1[2];

      edge1 = m_fsh.AllocateEdge(face1_corners[0], ON_SubDQuadFaceTopology_CopySectorWeight(edge0, vertex0), face1_corners[1], at_crease2_weight);
      if ( nullptr == edge1 )
        return ON_SUBD_RETURN_ERROR(false);
      face1_eptrs[0] = ON_SubDEdgePtr::Create(edge1, 0);

      edge1 = m_fsh.AllocateEdge(face1_corners[1], at_crease2_weight, face1_corners[2], ON_SubDSectorType::IgnoredSectorWeight);
      if ( nullptr == edge1 )
        return ON_SUBD_RETURN_ERROR(false);
      face1_eptrs[1] = ON_SubDEdgePtr::Create(edge1, 0);   

      face1_eptrs[2] = ON_SubDEdgePtr::Create(edge1_quartet[3],1);
      face1_eptrs[3] = ON_SubDEdgePtr::Create(edge1_quartet[2],1);

      face1 = m_fsh.AllocateQuad(zero_face_id, parent_face_id, face1_eptrs);
      if ( nullptr == face1 )
        return ON_SUBD_RETURN_ERROR(false);

      face0 = sit.NextFace(ON_SubDSectorIterator::StopAt::HardCrease);
      if ( face0 != face )
        return ON_SUBD_RETURN_ERROR(false);

      face0 = sit.NextFace(ON_SubDSectorIterator::StopAt::HardCrease);
      if ( face0 != neighbor0_duo[0] )
        return ON_SUBD_RETURN_ERROR(false);

      if (b3FaceCase)
        vertex1 = face1_corners[1];
      else
      {
        edge0 = sit.CurrentEdge(1);
        if ( nullptr == edge1 )
          return ON_SUBD_RETURN_ERROR(false);
        vertex1 = m_fsh.AllocateVertex(edge0,subd_type,bUseSavedSubdivisionPoint,3,2);
      }
      if ( nullptr == vertex1 )
        return ON_SUBD_RETURN_ERROR(false);
      face1_corners[3] = vertex1;
      face1_corners[1] = ring_vertex1[0];
      face1_corners[2] = const_cast<ON_SubDVertex*>(edge1_quartet[0]->m_vertex[1]);

      if (b3FaceCase)
      {
        face1_eptrs[3] = face1_eptrs[0].Reversed();
      }
      else
      {
        edge1 = m_fsh.AllocateEdge(face1_corners[0], ON_SubDQuadFaceTopology_CopySectorWeight(edge0, vertex0), face1_corners[3], at_crease2_weight );
        if ( nullptr == edge1 )
          return ON_SUBD_RETURN_ERROR(false);
        face1_eptrs[3] = ON_SubDEdgePtr::Create(edge1, 1);
      }

      face1_eptrs[0] = ON_SubDEdgePtr::Create(edge1_quartet[1], 1);
      face1_eptrs[1] = ON_SubDEdgePtr::Create(edge1_quartet[0], 0);
      edge1 = m_fsh.AllocateEdge(face1_corners[2],  ON_SubDSectorType::IgnoredSectorWeight, face1_corners[3], at_crease2_weight);
      if ( nullptr == edge1 )
        return ON_SUBD_RETURN_ERROR(false);
      face1_eptrs[2] = ON_SubDEdgePtr::Create(edge1, 0);

      face1 = m_fsh.AllocateQuad(zero_face_id, parent_face_id, face1_eptrs);
      if ( nullptr == face1 )
        return ON_SUBD_RETURN_ERROR(false);

      continue;
    }

    // general case 
    if (vertex0->IsCreaseOrCorner() && nullptr != neighbor0_duo[1])
    {
      // Back up (go clockwise) to an appropriate starting point.
      // Here the stop at = ON_SubDSectorIterator::StopAt::HardCrease because we are hopping
      // over an edge of the input face and the "other vertex" might be a dart.
      face0 = sit.PrevFace(ON_SubDSectorIterator::StopAt::Boundary);
      if (face0 != neighbor0_duo[1])
        return ON_SUBD_RETURN_ERROR(false);
      for (unsigned int sit_limit = 0; sit_limit <= vertex_face_count && face != face0; sit_limit++)
      {
        const ON_SubDFace* prev_face0 = face0;
        face0 = sit.PrevFace(ON_SubDSectorIterator::StopAt::Boundary);
        if (prev_face0 == face0)
          return ON_SUBD_RETURN_ERROR(false);

        if (nullptr == face0)
        {
          // Hit a boundary. Begin ccw iteration here
          if (nullptr == prev_face0)
            return ON_SUBD_RETURN_ERROR(false);
          if (vertex0 != sit.Initialize(prev_face0, 0, vertex0))
            return ON_SUBD_RETURN_ERROR(false);
          if (prev_face0 != sit.CurrentFace())
            return ON_SUBD_RETURN_ERROR(false);
          break;
        }

        if (face0 == face || face0 == neighbor0_duo[0])
        {
          // beginning ccw iteration at input face will work fine.
          if (vertex0 != sit.Initialize(face, 0, i))
            return ON_SUBD_RETURN_ERROR(false);
          face0 = nullptr;
          break;
        }

      }
      if (nullptr != face0)
        return ON_SUBD_RETURN_ERROR(false);
    }

    const bool bStopAtInputFace = (face == sit.CurrentFace());
    if (bStopAtInputFace)
    {
      if (nullptr == neighbor0_duo[0])
        return ON_SUBD_RETURN_ERROR(false);
      face0 = sit.NextFace(ON_SubDSectorIterator::StopAt::Boundary);
      if (face0 != neighbor0_duo[0])
        return ON_SUBD_RETURN_ERROR(false);
    }

    // This information is needed when vertex0 is a crease vertex, one of the neighboring
    // input face vertices is a dart, and sit is starting at a hard crease outside of the 
    // input face.
    const ON_SubDEdge* sit_first_edge0 = sit.CurrentEdge(0);
    if ( nullptr == sit_first_edge0 )
      return ON_SUBD_RETURN_ERROR(false);
    ON_SubDEdgePtr sit_first_eptr1 = ON_SubDEdgePtr::Null;

    face1_eptrs[0] = ON_SubDEdgePtr::Null;
    face1_eptrs[1] = ON_SubDEdgePtr::Null;
    face1_eptrs[2] = ON_SubDEdgePtr::Null;
    face1_eptrs[3] = ON_SubDEdgePtr::Null;

    bool bFinishedCorner = false;
    for (unsigned int sit_limit = 0; sit_limit < vertex_face_count; sit_limit++)
    {
      if (0 != sit_limit)
      {
        face0 = sit.NextFace(ON_SubDSectorIterator::StopAt::Boundary);
        if (nullptr == face0)
        {
          bFinishedCorner = true;
          break;
        }          
        edge0 = sit.CurrentEdge(0);
        if ( nullptr == edge0 )
          return ON_SUBD_RETURN_ERROR(false);
      }
      else
      {
        face0 = sit.CurrentFace();
        if (nullptr == face0)
          return ON_SUBD_RETURN_ERROR(false);
      }

      if (face == face0)
      {
        if ( bStopAtInputFace )
        {
          bFinishedCorner = true;
          break;
        }
        if (vertex0->IsCreaseOrCorner() && edge0_duo_bIsHardCrease[0])
        {
          if (edge0_duo[0] == sit.CurrentEdge(1))
          {
            bFinishedCorner = true;
            break;
          }
        }
        face1_eptrs[0] = ON_SubDEdgePtr::Create(edge1_quartet[2], 0);
        face1_eptrs[1] = ON_SubDEdgePtr::Null;
        face1_eptrs[2] = ON_SubDEdgePtr::Null;
        face1_eptrs[3] = ON_SubDEdgePtr::Create(edge1_quartet[1], 0);
        continue;
      }

      face1_eptrs[0] = face1_eptrs[3].Reversed();
      face1_eptrs[1] = ON_SubDEdgePtr::Null;
      face1_eptrs[2] = ON_SubDEdgePtr::Null;
      face1_eptrs[3] = ON_SubDEdgePtr::Null;

      if (face0 == neighbor0_duo[0])
      {
        face1_eptrs[0] = ON_SubDEdgePtr::Create(edge1_quartet[1], 1);
        face1_eptrs[1] = ON_SubDEdgePtr::Create(edge1_quartet[0], 0);
      }      
      if (face0 == neighbor0_duo[1])
      {
        face1_eptrs[2] = ON_SubDEdgePtr::Create(edge1_quartet[3], 1);
        face1_eptrs[3] = ON_SubDEdgePtr::Create(edge1_quartet[2], 1);
      }
      else if ((vertex_face_count-1) == sit_limit && sit_first_edge0 == sit.CurrentEdge(1) )
      {
        face1_eptrs[3] = sit_first_eptr1.Reversed();
      }

      face1_corners[1] = nullptr;
      face1_corners[2] = nullptr;
      face1_corners[3] = nullptr;
      for (int j = 1; j < 4;j++)
      {
        vertex1 = nullptr;
        for(;;)
        {
          vertex1 = const_cast<ON_SubDVertex*>(face1_eptrs[j-1].RelativeVertex(1));
          if (nullptr != vertex1)
            break;
          vertex1 = const_cast<ON_SubDVertex*>(face1_eptrs[j].RelativeVertex(0));
          if (nullptr != vertex1)
            break;
          switch (j)
          {
          case 1:
            {
              edge0 = sit.CurrentEdge(0);
              if (nullptr==edge0)
                return ON_SUBD_RETURN_ERROR(false);
              vertex1 = m_fsh.AllocateVertex(edge0,subd_type,bUseSavedSubdivisionPoint,3,2);
            }
            break;
          case 2:
            vertex1 = m_fsh.AllocateVertex(face0,subd_type,bUseSavedSubdivisionPoint,3,2);
            break;
          case 3:
            {
              edge0 = sit.CurrentEdge(1);
              if (nullptr == edge0)
                return ON_SUBD_RETURN_ERROR(false);
              vertex1 = m_fsh.AllocateVertex(edge0,subd_type,bUseSavedSubdivisionPoint,3,2);
            }
            break;
          }
          break;
        }
        if ( nullptr == vertex1 )
          return ON_SUBD_RETURN_ERROR(false);
        face1_corners[j] = vertex1;
      }

      for (int j = 0; j < 4; j++)
      {
        edge1 = ON_SUBD_EDGE_POINTER(face1_eptrs[j].m_ptr);
        if (nullptr == edge1)
        {
          switch (j)
          {
          case 0:
            {
              edge0 = sit.CurrentEdge(0);
              if (nullptr == edge0)
                return ON_SUBD_RETURN_ERROR(false);
              edge1 = m_fsh.AllocateEdge(
                face1_corners[0],
                ON_SubDQuadFaceTopology_CopySectorWeight(edge0, vertex0),
                face1_corners[1],
                at_crease2_weight
              );
              if ( 0 == sit_limit && edge0 == sit_first_edge0 )
                sit_first_eptr1 = ON_SubDEdgePtr::Create(edge1, 0);
            }
            break;
          case 1:
            edge1 = m_fsh.AllocateEdge(
              face1_corners[1],
              at_crease2_weight,
              face1_corners[2],
              ON_SubDSectorType::IgnoredSectorWeight
            );
            break;
          case 2:
            edge1 = m_fsh.AllocateEdge(
              face1_corners[2],
              ON_SubDSectorType::IgnoredSectorWeight,
              face1_corners[3],
              at_crease2_weight
            );
            break;
          case 3:
            {
              edge0 = sit.CurrentEdge(1);
              if (nullptr == edge0)
                return ON_SUBD_RETURN_ERROR(false);
              edge1 = m_fsh.AllocateEdge(
                face1_corners[3],
                at_crease2_weight,                
                face1_corners[0],
                ON_SubDQuadFaceTopology_CopySectorWeight(edge0, vertex0)
              );
            }
            break;
          }
          if ( nullptr == edge1 )
            return ON_SUBD_RETURN_ERROR(false);
          face1_eptrs[j] = ON_SubDEdgePtr::Create(edge1, 0);
        }
      }

      face1 = m_fsh.AllocateQuad(zero_face_id, parent_face_id, face1_eptrs);
      if ( nullptr == face1 )
        return ON_SUBD_RETURN_ERROR(false);
    }
    for(;;)
    {
      if (bFinishedCorner)
        break;

      edge0 = sit.CurrentEdge(1);
      if (nullptr != edge0 && edge0->IsHardCrease())
        break;

      return ON_SUBD_RETURN_ERROR(false);
    }
  }

  m_center_vertex1 = center_vertex1;
  m_subd_type = subd_type;
  m_face0 = face;
  m_face1 = m_center_vertex1->m_faces;
  m_face1_count = m_center_vertex1->m_face_count;

  return true;
}

#endif
